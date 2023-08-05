# -*- coding: utf-8 -*-
"""
Module: functions_crystallography.py

By Dan Porter, PhD
Diamond
2018

Usage: 
    - Run this file in an interactive console
    OR
    - from Dans_Diffraction import functions_crystallography as fc

Version 2.8
Last updated: 03/04/20

Version History:
09/07/15 0.1    Version History started.
30/10/17 1.0    Many updates
06/01/18 2.0    Renamed functions_crystallography.py
02/03/18 2.1    Removed call to tkinter
05/04/18 2.2    Added invert_sym
02/05/18 2.3    Added comparison of lower case elements and symmetry values
04/06/18 2.4    Added new checks to readcif, corrected atomic_properties for python3/numpy1.14
08/06/18 2.5    Corrected a few errors and added some more comments
06/03/19 2.6    Added print_atom_properties
14/08/19 2.7    Added new Dans Element Properties file with extra comment line, new functions added
03/04/20 2.8    Updated attenuation to work with arrays of elements

@author: DGPorter
"""

import sys, os, re
import numpy as np

from . import functions_general as fg

__version__ = '2.7'

# File directory - location of "Dans Element Properties.txt"
datadir = os.path.abspath(os.path.dirname(__file__))  # same directory as this file
datadir = os.path.join(datadir, 'data')


def getenergy():
    return 8.048  # Cu Kalpha energy, keV


'--------------Functions to Load crystal Structures----------------------'


def readcif(filename=None, debug=False):
    """
    Open a Crystallographic Information File (*.cif) file and store all entries in a key:value dictionary
     Looped values are stored as lists under a single key entry
     All values are stored as strings
    E.G.
      crys=readcif('somefile.cif')
      crys['_cell_length_a'] = '2.835(2)'

    crys[key] = value
    available keys are give by crys.keys()

    To debug the file with outputted messages, use:
      cif = readcif(file, debug=True)

    Some useful standard CIF keywords:
        _cell_length_a
        _cell_length_b
        _cell_length_c
        _cell_angle_alpha
        _cell_angle_beta
        _cell_angle_gamma
        _space_group_symop_operation_xyz
        _atom_site_label
        _atom_site_type_symbol
        _atom_site_occupancy
        _atom_site_U_iso_or_equiv
        _atom_site_fract_x
        _atom_site_fract_y
        _atom_site_fract_z
    """

    # Get file name
    (dirName, filetitle) = os.path.split(filename)
    (fname, Ext) = os.path.splitext(filetitle)

    # Open file
    file = open(filename)
    text = file.read()
    file.close()

    # Remove blank lines
    while "\n\n" in text:
        text = text.replace("\n\n", "\n")
    lines = text.splitlines()

    cifvals = {}
    cifvals['Filename'] = filename
    cifvals['Directory'] = dirName
    cifvals['FileTitle'] = fname

    # Read file line by line, converting the cif file values to a python dict
    n = 0
    while n < len(lines):
        # Convert line to columns
        vals = lines[n].split()

        # skip empty lines
        if len(vals) == 0:
            n += 1
            continue

        # Search for stored value lines
        if vals[0][0] == '_':
            if len(vals) > 2 and ('\'' in vals[1] or '"' in vals[1]):
                # catch strings with spaces
                cifvals[vals[0]] = ' '.join(vals[1:]).strip('\'"')
            elif len(vals) == 1 and ';' in lines[n + 1]:
                # Catch multi-line arguments
                n += 1
                cifvals[vals[0]] = [lines[n].strip().replace(';', '')]
                n += 1
                while ';' not in lines[n]:
                    cifvals[vals[0]] += [lines[n].strip()]
                    n += 1
                cifvals[vals[0]] = ' '.join(cifvals[vals[0]])
            elif len(vals) > 1:
                cifvals[vals[0]] = vals[1]
            n += 1

            if debug:
                print('%5d %s = %s' % (n, vals[0], cifvals[vals[0]]))
            continue

        # Search for loops
        elif vals[0] == 'loop_':
            n += 1
            loopvals = []
            # Step 1: Assign loop columns
            # looped columns are given by "_column_name"
            while n < len(lines) and len(lines[n].strip()) > 0 and lines[n].strip()[
                0] == '_':  # 21/5/18 split()[0][0] == '_':
                loopvals += [lines[n].split()[0]]
                cifvals[loopvals[-1]] = []
                n += 1

            # Skip blank line after column names, e.g. 1000175.cif 21/5/18
            # if len(lines[n].strip()) == 0: n += 1

            # Step 2: Assign data to columns
            # loops until line has less segments than columns
            while n < len(lines) and len(lines[n].split()) >= len(loopvals):
                cols = lines[n].split()
                cols = cols[:len(loopvals) - 1] + [
                    ''.join(cols[len(loopvals) - 1:])]  # fixes error on symmetry arguments having spaces
                if cols[0][0] == '_' or cols[0] == 'loop_': break  # catches error if loop is only 1 iteration
                if len(loopvals) == 1:
                    cifvals[loopvals[0]] += [lines[n].strip()]
                else:
                    for c, ll in enumerate(loopvals):
                        cifvals[ll] += [cols[c]]
                n += 1

            if debug:
                for ll in loopvals:
                    print('%5d %s = %s' % (n, ll, str(cifvals[ll])))
            continue

        else:
            # Skip anything else
            n += 1

    # Replace '.' in keys - fix bug from isodistort cif files
    # e.g. '_space_group_symop_magn_operation.xyz'
    current_keys = list(cifvals.keys())
    for key in current_keys:
        if '.' in key:
            newkey = key.replace('.', '_')
            cifvals[newkey] = cifvals[key]
    return cifvals


def cif2dict(cifvals):
    """
    From a dict of key:value pairs generated from a *.cif file (using readcif),
    read standard crystallographic infromation into a crystal dictionary, with keys:
        'filename' - cif filename
        'name' - name of structure
        'unit vector'   - [3x3] array of basis vectors [a,b,c]
        'parent cell'   - [3x3] array of parent basis vectors [a,b,c]
        'symmetry'      - list of string symmetry operations
        'space group'   - Space Group string
        'space group number' - Space group number
        'cif'           - cif dict
        The following are specific to atomis within the unit cell:
        'atom type'     - list of elements e.g. ['Co','O', 'O']
        'atom label'    - list of atom site names e.g. ['Co1, 'O1', 'O2']
        'atom position' - [nx3] array of atomic positions
        'atom occupancy'- [nx1] array of atom site occupancies
        'atom uiso'     - [nx1] array of atom site isotropic thermal parameters
        'atom uaniso'   - [nx6] array of atom site anisotropic thermal parameters
        'mag moment'    - [nx3] array of atom site magnetic moment vectors
        'mag time'      - [nx3] array of atom site magnetic time symmetry
        'misc'] = [element, label, cif_pos, occ, Uiso]
    :param cifvals: dict from readcif
    :return: dict
    """

    keys = cifvals.keys()

    # Generate unit vectors
    a, da = fg.readstfm(cifvals['_cell_length_a'])
    b, db = fg.readstfm(cifvals['_cell_length_b'])
    c, dc = fg.readstfm(cifvals['_cell_length_c'])
    alpha, dalpha = fg.readstfm(cifvals['_cell_angle_alpha'])
    beta, dbeta = fg.readstfm(cifvals['_cell_angle_beta'])
    gamma, dgamma = fg.readstfm(cifvals['_cell_angle_gamma'])
    UV = latpar2UV(a, b, c, alpha, beta, gamma)

    # Get atom names & labels
    label = cifvals['_atom_site_label']

    if '_atom_site_type_symbol' in keys:
        element = [x.strip('+-0123456789') for x in cifvals['_atom_site_type_symbol']]
    else:
        element = [x.strip('+-0123456789') for x in cifvals['_atom_site_label']]

    # Get other properties
    if '_atom_site_U_iso_or_equiv' in keys:
        Uiso = np.array([fg.readstfm(x)[0] for x in cifvals['_atom_site_U_iso_or_equiv']])
    elif '_atom_site_B_iso_or_equiv' in keys:
        biso = np.array([fg.readstfm(x)[0] for x in cifvals['_atom_site_B_iso_or_equiv']])
        Uiso = biso2uiso(biso)
    else:
        Uiso = np.zeros(len(element))
    if '_atom_site_occupancy' in keys:
        occ = np.array([fg.readstfm(x)[0] for x in cifvals['_atom_site_occupancy']])
    else:
        occ = np.ones(len(element))

    # Get coordinates
    u = np.array([fg.readstfm(x)[0] for x in cifvals['_atom_site_fract_x']])
    v = np.array([fg.readstfm(x)[0] for x in cifvals['_atom_site_fract_y']])
    w = np.array([fg.readstfm(x)[0] for x in cifvals['_atom_site_fract_z']])
    cif_pos = np.array([u, v, w]).T

    # Get magnetic vectors
    cif_vec = np.zeros(cif_pos.shape)
    cif_mag = np.zeros(len(u))
    if '_atom_site_moment_label' in keys:
        mag_atoms = cifvals['_atom_site_moment_label']
        mx = np.array([fg.readstfm(x)[0] for x in cifvals['_atom_site_moment_crystalaxis_x']])
        my = np.array([fg.readstfm(x)[0] for x in cifvals['_atom_site_moment_crystalaxis_y']])
        mz = np.array([fg.readstfm(x)[0] for x in cifvals['_atom_site_moment_crystalaxis_z']])
        mag_pos = np.array([mx, my, mz]).T
        for n, ma in enumerate(mag_atoms):
            mag_idx = label.index(ma)
            cif_vec[mag_idx, :] = mag_pos[n, :]
            cif_mag[mag_idx] = fg.mag(mag_pos[n, :])

    # Get symmetry operations
    if '_symmetry_equiv_pos_as_xyz' in keys:
        symops = cifvals['_symmetry_equiv_pos_as_xyz']
        symtim = [1] * len(symops)
        symmag = ['mx,my,mz'] * len(symops)
        symcen = ['x,y,z']
        symcentim = [1]
        symcenmag = ['mx,my,mz']
    elif '_space_group_symop_operation_xyz' in keys:
        symops = cifvals['_space_group_symop_operation_xyz']
        symtim = [1] * len(symops)
        symmag = ['mx,my,mz'] * len(symops)
        symcen = ['x,y,z']
        symcentim = [1]
        symcenmag = ['mx,my,mz']
    elif '_space_group_symop.magn_operation_xyz' in keys:
        symops_tim = cifvals['_space_group_symop.magn_operation_xyz']
        # Each symop given with time value: x,y,z,+1, separate them:
        symops = [','.join(s.split(',')[:3]) for s in symops_tim]  # x,y,z
        symtim = [np.int(s.split(',')[-1]) for s in symops_tim]  # +1
        symmag = cifvals['_space_group_symop.magn_operation_mxmymz']

        # Centring vectors also given in this case
        symcen_tim = cifvals['_space_group_symop.magn_centering_xyz']
        symcen = [','.join(s.split(',')[:3]) for s in symcen_tim]  # x,y,z
        symcentim = [np.int(s.split(',')[-1]) for s in symcen_tim]  # +1
        symcenmag = cifvals['_space_group_symop.magn_centering_mxmymz']
    else:
        symops = ['x,y,z']
        symtim = [1]
        symmag = ['mx,my,mz']
        symcen = ['x,y,z']
        symcentim = [1]
        symcenmag = ['mx,my,mz']
    symops = [re.sub('\'', '', x) for x in symops]
    symmag = [sm.replace('m', '') for sm in symmag]  # remove m
    symcenmag = [sm.replace('m', '') for sm in symcenmag]  # remove m

    # Get magnetic symmetry constraints
    if '_magnetic_atom_site_moment_symmetry_constraints_label' in keys:
        const_labels = cifvals['_magnetic_atom_site_moment_symmetry_constraints_label']
        constraints = cifvals['_atom_site_magnetic_moment_symmetry_constraints_mxmymz']
    else:
        const_labels = []
        constraints = []

    # apply symmetry operations to each position, generating P1 structure
    # Also repeat each element property
    NsymOps = len(symops)
    NcenOps = len(symcen)
    Nops = NsymOps * NcenOps
    p1pos = np.empty([0, 3])
    p1vec = np.empty([0, 3])
    p1mag = []
    p1typ = []
    p1lbl = []
    p1occ = []
    p1Uiso = []
    p1tim = []
    for n, (x, y, z) in enumerate(cif_pos):
        uvw = gen_sym_pos(symops, x, y, z)
        uvw = fitincell(uvw)

        # Apply symmetry constraints
        if label[n] in const_labels:
            # Assumes single constraint per atom
            idx = const_labels.index(label[n])
            C = constraints[idx]
            C = C.replace('m', '')
            # print('Constraint: {:3s} {:s}'.format(label[n],C))
            # convert '2x' to 'x'
            old = re.findall('\d[xyz]', C)
            new = [s.replace('x', '*x').replace('y', '*y').replace('z', '*z') for s in old]
            for s in range(len(old)):
                C = C.replace(old[s], new[s])
            C = C.split(',')
            # Apply constraint to symmetry arguments
            S = [s.replace('x', 'a').replace('y', 'b').replace('z', 'c') for s in symmag]
            S = [s.replace('a', C[0]).replace('b', C[1]).replace('c', C[2]) for s in S]
        else:
            S = symmag

        mx, my, mz = cif_vec[n]
        mag_uvw = gen_sym_pos(S, mx, my, mz)
        # print('---{:3.0f}. {:2s} ({:5.2f},{:5.2f},{:5.2f})---'.format(n,label[n],mx,my,mz))

        # Loop over centring operations
        sympos = np.zeros([Nops, 3])
        symmagpos = np.zeros([Nops, 3])
        symtimpos = np.zeros(Nops)
        for m, (cx, cy, cz) in enumerate(uvw):
            Ni, Nj = m * NcenOps, (m + 1) * NcenOps
            cen_uvw = gen_sym_pos(symcen, cx, cy, cz)
            cen_uvw = fitincell(cen_uvw)
            sympos[Ni:Nj, :] = cen_uvw

            cmx, cmy, cmz = mag_uvw[m]
            mag_cen = gen_sym_pos(symcenmag, cmx, cmy, cmz)
            # print('  Sym{:2.0f}: {:10s} ({:5.2f},{:5.2f},{:5.2f})'.format(m,S[m],cmx,cmy,cmz))
            # for o in range(len(mag_cen)):
            # print('    Cen{:1.0f}: {:10s} ({:5.2f},{:5.2f},{:5.2f})'.format(o,symcenmag[o],*mag_cen[o]))
            symmagpos[Ni:Nj, :] = mag_cen
            symtimpos[Ni:Nj] = symtim[m] * np.array(symcentim)

        # Remove duplicates
        newarray, uniqueidx, matchidx = fg.unique_vector(sympos, 0.01)
        cen_uvw = sympos[uniqueidx, :]
        mag_cen = symmagpos[uniqueidx, :]
        symtimpos = symtimpos[uniqueidx]

        # Append to P1 atoms arrays
        p1pos = np.append(p1pos, cen_uvw, axis=0)
        p1vec = np.append(p1vec, mag_cen, axis=0)
        p1mag = np.append(p1mag, np.repeat(cif_mag[n], len(cen_uvw)))
        p1tim = np.append(p1tim, symtimpos)
        p1typ = np.append(p1typ, np.repeat(element[n], len(cen_uvw)))
        p1lbl = np.append(p1lbl, np.repeat(label[n], len(cen_uvw)))
        p1occ = np.append(p1occ, np.repeat(occ[n], len(cen_uvw)))
        p1Uiso = np.append(p1Uiso, np.repeat(Uiso[n], len(cen_uvw)))

    # Get space group
    if '_symmetry_space_group_name_H-M' in keys:
        spacegroup = cifvals['_symmetry_space_group_name_H-M']
    elif '_space_group_name_H-M_alt' in keys:
        spacegroup = cifvals['_space_group_name_H-M_alt']
    elif len(symops) == 1:
        spacegroup = 'P1'
    else:
        spacegroup = ''
    if '_symmetry_Int_Tables_number' in keys:
        sgn = float(cifvals['_symmetry_Int_Tables_number'])
    elif '_space_group_IT_number' in keys:
        sgn = float(cifvals['_space_group_IT_number'])
    elif spacegroup == 'P1':
        sgn = 1
    else:
        sgn = 0

    # print mag_pos
    # print p1mag
    # print p1vec
    # print fg.mag(p1vec)
    # Add values to the dict
    crys = {}
    crys['filename'] = cifvals['Filename']
    crys['name'] = cifvals['FileTitle']
    crys['unit vector'] = UV
    crys['parent cell'] = UV
    crys['origin'] = np.array([[0., 0., 0.]])
    crys['symmetry'] = symops
    crys['atom type'] = p1typ
    crys['atom label'] = p1lbl
    crys['atom position'] = p1pos
    crys['atom occupancy'] = p1occ
    crys['atom uiso'] = p1Uiso
    crys['atom uaniso'] = np.zeros([len(p1pos), 6])
    crys['mag moment'] = p1vec
    crys['mag time'] = p1tim
    crys['normalise'] = 1.
    crys['misc'] = [element, label, cif_pos, occ, Uiso]
    crys['space group'] = spacegroup
    crys['space group number'] = sgn
    crys['cif'] = cifvals
    return crys


def read_atom_properties_file(filedir):
    """
    Reads the text file "Dans Element Properties.txt"
    Returns a list of dicts containing atomic properites from multiple sources
      data = read_atom_properties_file(filedir)
      data[22]['Element']
    :param filedir: location of "Dans Element Properties.txt"
    :return: [dict, ...]
    """
    with open(filedir, 'rt') as f:
        lines = f.readlines()

    head = None
    data = []
    for line in lines:
        # Header
        if '#' in line: continue
        if head is None: head = line.split(); continue
        # Data
        vals = line.split()
        element = {}
        for n in range(len(vals)):
            try:
                value = int(vals[n])
            except ValueError:
                try:
                    value = float(vals[n])
                except ValueError:
                    value = vals[n]
            element[head[n]] = value
        data += [element]
    return data


def atom_properties(elements=None, fields=None):
    """
    Loads the atomic properties of a particular atom from a database

    Usage:
            A = atom_properties() >> returns structured array of all properties for all atoms A[0]['Element']='H'
            A = atom_properties('Co') >> returns structured array of all properties for 1 element
            B = atom_properties('Co','Weight') >> returns regular 1x1 array
            B = atom_properties(['Co','O'],'Weight') >> retruns regular 2x1 array
            A = atom_properties('Co',['a1','b1','a2','b2','a3','b3','a4','b4','c']) >> returns structured array of requested properties
            A = atom_properties(['Co','O'],['Z','Weight']) >> returns 2x2 structured array

    Available properties:
        A = atom_properties()
        print(A.dtype.names)

    Available information includes:
          Z             = Element number
          Element Name  = Element name
          Group         = Element Group on periodic table
          Period        = Element period on periodic table
          Block         = Element electronic block (s,p,d,f)
          ValenceE      = Number of valence electrons
          Config        = Element electronic orbital configuration
          Radii         = Atomic Radii (pm)
          Weight        = Standard atomic weight (g)
          Coh_b         = Bound coherent neutron scattering length
          Inc_b         = Bound incoherent neutron scattering length
          Nabs          = Neutron absorption coefficient
          Nscat         = Neutron scattering coefficient
          a1            = Electron form factor
          b1            = Electron form factor
          a2            = Electron form factor
          b2            = Electron form factor
          a3            = Electron form factor
          b3            = Electron form factor
          a4            = Electron form factor
          b4            = Electron form factor
          c             = Electron form factor
          j0_A          = Magnetic Form factor
          j0_a          = Magnetic Form factor
          j0_B          = Magnetic Form factor
          j0_b          = Magnetic Form factor
          j0_C          = Magnetic Form factor
          j0_c          = Magnetic Form factor
          j0_D          = Magnetic Form factor
          K             = x-ray absorption edge
          L1            = x-ray absorption edge
          L2            = x-ray absorption edge
          L3            = x-ray absorption edge
          M1...         = x-ray absorption edge
    """

    atomfile = os.path.join(datadir, 'Dans Element Properties.txt')
    try:
        data = np.genfromtxt(atomfile, skip_header=6, dtype=None, names=True, encoding='ascii')
    except TypeError:
        # Numpy version < 1.14
        data = np.genfromtxt(atomfile, skip_header=6, dtype=None, names=True)

    if elements is not None:
        # elements must be a list e.g. ['Co','O']
        elements = np.char.lower(np.asarray(elements).reshape(-1))
        indx = [None] * len(elements)
        for n in range(len(data)):
            d = data[n]
            fileelement = d['Element'].lower()
            if fileelement in elements:
                for m in range(len(elements)):
                    if fileelement == elements[m]:
                        indx[m] = n
        data = data[indx]

    if fields is None:
        return data

    return data[fields]


def print_atom_properties(elements=None):
    """
    Outputs string of stored atomic properties
    :param elements: str or list or None
            str: 'Co'
            list: ['Co', 'O']
    :return: str
    """

    prop = atom_properties(elements)
    keys = prop.dtype.names
    elename = ' '.join(['%10s'%ele for ele in prop['Element']])
    out = '%8s : %s\n'%('', elename)
    for key in keys:
        propval = ' '.join(['%10s'%ele for ele in prop[key]])
        out += '%8s : %s\n' % (key, propval)
    return out


def xray_scattering_factor(element, Qmag=0):
    """
    Read X-ray scattering factor table, calculate f(|Q|)
    Uses the oefficients for analytical approximation to the scattering factors - ITC, p578
     Qff = read_xsf(element,Qmag=[0])
    """

    # Qmag should be a 1D array
    Qmag = np.asarray(Qmag).reshape(-1)

    coef = atom_properties(element, ['a1', 'b1', 'a2', 'b2', 'a3', 'b3', 'a4', 'b4', 'c'])

    Qff = np.zeros([len(Qmag), len(coef)])

    for n in range(len(coef)):
        a1 = coef['a1'][n]
        b1 = coef['b1'][n]
        a2 = coef['a2'][n]
        b2 = coef['b2'][n]
        a3 = coef['a3'][n]
        b3 = coef['b3'][n]
        a4 = coef['a4'][n]
        b4 = coef['b4'][n]
        c = coef['c'][n]

        f = a1 * np.exp(-b1 * (Qmag / (4 * np.pi)) ** 2) + \
            a2 * np.exp(-b2 * (Qmag / (4 * np.pi)) ** 2) + \
            a3 * np.exp(-b3 * (Qmag / (4 * np.pi)) ** 2) + \
            a4 * np.exp(-b4 * (Qmag / (4 * np.pi)) ** 2) + c
        Qff[:, n] = f
    return Qff


def magnetic_form_factor(element, Qmag=0.):
    """
    Read Magnetic form factor table, calculate <j0(|Q|)>
    Analytical approximation of the magnetic form factor:
        <j0(|Q|)> = A*exp(-a*s^2) + B*exp(-b*s^2) + C*exp(-c*s^2) + D, where s = sin(theta)/lambda in A-1
    See more about the approximatio here: https://www.ill.eu/sites/ccsl/ffacts/ffactnode3.html
    Note: Currently only J0 terms are used and 5d atoms are not currently included
    Usage:
         Qff = read_mff(element,Qmag)
         element = str element name, e.g. 'Co'
         Qmag = magnitude of Q=sin(theta)/lambda in A-1 at which to calcualte, can be a list or array to return multiple values
         Qff = Magnetic form factor for element at Qmag
    E.G.
        Qff = read_mff('Co',np.arange(0,4,0.1))
    """

    # Qmag should be a 1D array
    Qmag = np.asarray(Qmag).reshape(-1)

    coef = atom_properties(element, ['j0_A', 'j0_a', 'j0_B', 'j0_b', 'j0_C', 'j0_c', 'j0_D'])

    # Nqpointings x Nelements
    Qff = np.zeros([len(Qmag), len(coef)])

    # Loop over elements
    for n in range(len(coef)):
        A = coef['j0_A'][n]
        a = coef['j0_a'][n]
        B = coef['j0_B'][n]
        b = coef['j0_b'][n]
        C = coef['j0_C'][n]
        c = coef['j0_c'][n]
        D = coef['j0_D'][n]

        j0 = A * np.exp(-a * Qmag ** 2) + \
             B * np.exp(-b * Qmag ** 2) + \
             C * np.exp(-c * Qmag ** 2) + D
        Qff[:, n] = j0
    return Qff


def debyewaller(uiso, Qmag=[0]):
    """
    Calculate the debye waller factor for a particular Q
     T = debyewaller(uiso,Qmag=[0])

        T = exp( -2*pi^2*Uiso/d^2 )
        T = exp( -Uiso/2Q^2 )
    """

    # Qmag should be a 1D array
    Qmag = np.asarray(Qmag).reshape(-1)

    uiso = np.asarray(uiso, dtype=np.float).reshape(1, -1)
    Qmag = np.asarray(Qmag, dtype=np.float).reshape(-1, 1)
    Tall = np.exp(-0.5 * np.dot(Qmag, uiso))
    # Tall = np.zeros([len(Qmag),len(uiso)])
    # Generate the approximation for each atom
    # for n in range(len(uiso)):
    #    for m in range(len(Qmag)):
    #        # Definition of Debye-Waller factor from Vesta user manual p45
    #        Tall[m,n] = dnp.exp(-0.5*uiso[n]*Qmag[m])
    return Tall


def attenuation(element_z, energy_keV):
    """
     Returns the x-ray mass attenuation, u/p, in cm^2/g
       e.g. A = attenuation(23,np.arange(7,8,0.01)) # Cu
            A = attenuation([23,24,25], 5.6)
            a = attenuation(19,4.5) # K
    """
    element_z = np.asarray(element_z).reshape(-1)
    energy_keV = np.asarray(energy_keV).reshape(-1)

    xma_file = os.path.join(datadir, 'XRayMassAtten_mup.dat')
    xma_data = np.loadtxt(xma_file)

    energies = xma_data[:, 0] / 1000.
    out = np.zeros([len(energy_keV), len(element_z)])
    for n, z in enumerate(element_z):
        out[:, n] = np.interp(energy_keV, energies, xma_data[:, z])
    if len(element_z) == 1:
        return out[:, 0]
    return out


'--------------Element Properties & Charge----------------------'


def element_symbol(element_Z):
    """
    Returns the element sympol for element_Z
    :param element_Z: int
    :return: str
    """
    symbols = atom_properties(None, 'Element')
    return symbols[element_Z-1]


def element_z(element):
    """
    Returns the element number Z
    :param element: str
    :return: int
    """
    z = atom_properties(element, 'Z')
    if len(z) == 1:
        return z[0]
    return z


def orbital_configuration(element_Z):
    """
    Returns the orbital configuration of an element as a list of strings
    :param element_Z: int
    :return: ['1s2', '2s2', '2p6', ...]
    """

    config = atom_properties(element_symbol(element_Z), 'Config')
    return config[0].split('.')


def split_element_symbol(element):
    """
    From element symbol, split charge and occupancy
      symbol, occupancy, charge = split_element_symbol('Co3+')
    :param element: str
    :return: symbol: str
    :return: occupancy: float
    :return: charge: float
    """

    atom_n = re.findall('[A-Z][a-z]?|[0-9]+[.]?[0-9]*', element)
    symbol = atom_n[0]
    charge = 0
    occupancy = 1
    if len(atom_n) > 1:
        if '-' in element:
            charge = -float(atom_n[1])
        elif '+' in element:
            charge = float(atom_n[1])
        else:
            occupancy = float(atom_n[1])
    return symbol, occupancy, charge


def default_atom_charge(element):
    """
    Returns the default charge value for the element
    :param element: str: 'Fe'
    :return: int or nan
    """

    element = np.asarray(element).reshape(-1)
    charge = np.zeros(len(element))
    for n in range(len(element)):
        symbol, occupancy, elecharge = split_element_symbol(element[n])
        group = atom_properties(symbol, 'Group')[0]
        if elecharge != 0:
            charge[n] = elecharge
        elif group == 1:
            charge[n] = 1*occupancy
        elif group == 2:
            charge[n] = 2*occupancy
        elif group == 16:
            charge[n] = -2*occupancy
        elif group == 17:
            charge[n] = -1*occupancy
        elif group == 18:
            charge[n] = 0
        else:
            charge[n] = np.nan
    if len(charge) == 1:
        return charge[0]
    return charge


def balance_atom_charge(list_of_elements, occupancy=None):
    """
    Determine the default charges and assign remaining charge to
    unspecified elements
    :param list_of_elements:
    :return: [list of charges]
    """

    if occupancy is None:
        occupancy = np.ones(len(list_of_elements))
    else:
        occupancy = np.asarray(occupancy)

    charge = np.zeros(len(list_of_elements))
    for n in range(len(list_of_elements)):
        _, occ, _ = split_element_symbol(list_of_elements[n])
        charge[n] = occupancy[n]*default_atom_charge(list_of_elements[n])
        occupancy[n] = occupancy[n]*occ

    remaining_charge = -np.nansum(charge)
    uncharged = np.sum(occupancy[np.isnan(charge)])
    for n in range(len(list_of_elements)):
        if np.isnan(charge[n]):
            charge[n] = occupancy[n]*remaining_charge/uncharged
    return charge


def arrange_atom_order(list_of_elements):
    """
    Arrange a list of elements in the correct chemical order
      ['Li','Co','O'] = arrange_atom_order(['Co', 'O', 'Li'])
    :param list_of_elements: [list of str]
    :return: [list of str]
    """

    list_of_elements = np.asarray(list_of_elements)
    group = atom_properties(list_of_elements, 'Group')
    idx = np.argsort(group)
    return list(list_of_elements[idx])


def count_atoms(list_of_elements, occupancy=None, divideby=1, latex=False):
    """
    Count atoms in a list of elements, returning condenced list of elements
    :param list_of_elements: list of element symbols
    :param occupancy: list of occupancies of each element (default=None)
    :param divideby: divide each count by this (default=1)
    :param latex: False*/True
    :return: [list of str]
    """

    if occupancy is None:
        occupancy = np.ones(len(list_of_elements))

    # Count elements
    ats = np.unique(list_of_elements)
    ats = arrange_atom_order(ats)  # arrange this by alcali/TM/O
    outstr = []
    for a in ats:
        atno = sum([occupancy[n] for n, x in enumerate(list_of_elements) if x == a])/float(divideby)
        if np.abs(atno - 1) < 0.01:
            atstr = ''
        else:
            atstr = '%0.2g' % atno
            if latex:
                atstr = '$_{%s}$' % atstr

        outstr += ['%s%s' % (a, atstr)]
    return outstr


def count_charges(list_of_elements, occupancy=None, divideby=1, latex=False):
    """
    Count atoms in a list of elements, returning condenced list of elements with charges
    :param list_of_elements: list of element symbols
    :param occupancy: list of occupancies of each element (default=None)
    :param divideby: divide each count by this (default=1)
    :param latex: False*/True
    :return: [list of str]
    """

    if occupancy is None:
        occupancy = np.ones(len(list_of_elements))

    # Determine element charges
    charge = balance_atom_charge(list_of_elements, occupancy)

    # Count elements
    ats = np.unique(list_of_elements)
    ats = arrange_atom_order(ats)  # arrange this by alcali/TM/O
    atno = {}
    chno = {}
    for a in ats:
        atno[a] = sum([occupancy[n] for n, x in enumerate(list_of_elements) if x == a])/float(divideby)
        chno[a] = sum([charge[n] for n, x in enumerate(list_of_elements) if x == a])/(atno[a]*float(divideby))

    outstr = []
    for a in ats:
        if np.abs(chno[a]-1) < 0.01:
            chstr = '+'
        elif np.abs(chno[a]+1) < 0.01:
            chstr = '-'
        elif chno[a] > 0:
            chstr = '%0.2g+' % chno[a]
        else:
            chstr = '%0.2g-' % abs(chno[a])

        if latex:
            chstr = '$^{%s}$' % chstr

        if np.abs(atno[a]-1) < 0.01:
            outstr += ['%s%s' % (a, chstr)]
        else:
            outstr += ['%0.2g[%s%s]' % (atno[a], a, chstr)]
    return outstr


'-------------------Lattice Transformations------------------------------'


def RcSp(UV):
    """
    Generate reciprocal cell from real space unit vecors
    Usage:
    UVs = RcSp(UV)
      UV = [[3x3]] matrix of vectors [a,b,c]
    """

    # b1 = 2*np.pi*np.cross(UV[1],UV[2])/np.dot(UV[0],np.cross(UV[1],UV[2]))
    # b2 = 2*np.pi*np.cross(UV[2],UV[0])/np.dot(UV[0],np.cross(UV[1],UV[2]))
    # b3 = 2*np.pi*np.cross(UV[0],UV[1])/np.dot(UV[0],np.cross(UV[1],UV[2]))
    # UVs = np.array([b1,b2,b3])

    UVs = 2 * np.pi * np.linalg.inv(UV).T
    return UVs


def indx(Q, UV):
    """
    Index Q(x,y,z) on on lattice [h,k,l] with unit vectors UV
    Usage:
      HKL = indx(Q,UV)
      Q = [[nx3]] array of vectors
      UV = [[3x3]] matrix of vectors [a,b,c]
    """
    HKL = np.dot(Q, np.linalg.inv(UV))
    return HKL


def Bmatrix(UV):
    """
    Calculate the Busing and Levy B matrix from a real space UV
    """

    a1, a2, a3 = fg.mag(UV)
    alpha3 = fg.ang(UV[0, :], UV[1, :])
    alpha2 = fg.ang(UV[0, :], UV[2, :])
    alpha1 = fg.ang(UV[1, :], UV[2, :])
    # print a1,a2,a3
    # print alpha1,alpha2,alpha3
    UVs = RcSp(UV) / (2 * np.pi)
    b1, b2, b3 = fg.mag(UVs)
    beta3 = fg.ang(UVs[0, :], UVs[1, :])
    beta2 = fg.ang(UVs[0, :], UVs[2, :])
    beta1 = fg.ang(UVs[1, :], UVs[2, :])
    # print b1,b2,b3
    # print beta1,beta2,beta3

    B = np.array([[b1, b2 * np.cos(beta3), b3 * np.cos(beta2)],
                  [0, b2 * np.sin(beta3), -b3 * np.sin(beta2) * np.cos(alpha1)],
                  [0, 0, 1 / a3]])
    return B


def maxHKL(Qmax, UV):
    """
    Returns the maximum indexes for given max radius
    e.g.
        UVstar = RcSp([[3,0,0],[0,3,0],[0,0,10]]) # A^-1
        Qmax = 4.5 # A^-1
        max_hkl = maxHKL(Qmax,UVstar)
        max_hkl =
        >>> [3,3,8]
    """

    Qpos = [[Qmax, Qmax, Qmax],
            [-Qmax, Qmax, Qmax],
            [Qmax, -Qmax, Qmax],
            [-Qmax, -Qmax, Qmax],
            [Qmax, Qmax, -Qmax],
            [-Qmax, Qmax, -Qmax],
            [Qmax, -Qmax, -Qmax],
            [-Qmax, -Qmax, -Qmax]]
    hkl = indx(Qpos, UV)
    return np.ceil(np.abs(hkl).max(axis=0)).astype(int)


def genHKL(H, K=None, L=None):
    """
    Generate HKL array with all combinations within range specified
    Usage:
      HKL = genHKL(max)
       int max = generates each h,k,l from -max to max
      HKL = genHKL([min,max])
       int min, int max = generates h,l,l from min to max
      HKL = genHKL([hmin,hmax],[kmin,kmax],[lmin,lmax])
       hmin,hmax = min and max values for h, k and l respectivley

      array HKL = [[nx3]] array of [h,k,l] vectors

    E.G.
      HKL = genHKL(-3)
    E.G.
      HKL = genHKL([-1,1])
    E.G.
      HKL = genHKL([-2,2],[0,3],[1,1])
    """

    if K is None: K = H
    if L is None: L = H

    H = np.asarray(H)
    K = np.asarray(K)
    L = np.asarray(L)

    if H.size == 1:
        H = np.array([H, -H])
    if K.size == 1:
        K = np.array([K, -K])
    if L.size == 1:
        L = np.array([L, -L])

    if H[0] > H[1]:
        Hstep = -1
    else:
        Hstep = 1
    if K[0] > K[1]:
        Kstep = -1
    else:
        Kstep = 1.0
    if L[0] > L[1]:
        Lstep = -1.0
    else:
        Lstep = 1.0

    Hrange = np.arange(H[0], H[1] + Hstep, Hstep)
    Krange = np.arange(K[0], K[1] + Kstep, Kstep)
    Lrange = np.arange(L[0], L[1] + Lstep, Hstep)
    KK, HH, LL = np.meshgrid(Krange, Hrange, Lrange)

    return np.asarray([HH.ravel(), KK.ravel(), LL.ravel()], dtype=int).T


def fitincell(uvw):
    """
    Set all fractional coodinates between 0 and 1
    Usage:
      uvw = fitincell(uvw)
      uvw = [[nx3]] array of fractional vectors [u,v,w]
    """
    while np.any(uvw > 0.99) or np.any(uvw < -0.01):
        uvw[uvw > 0.99] = uvw[uvw > 0.99] - 1.
        uvw[uvw < -0.01] = uvw[uvw < -0.01] + 1.
    return uvw


def gen_sym_pos(sym_ops, x, y, z):
    """
    Generate positions from symmetry operations
    Usage:
      uvw = gen_sym_pos(sym_ops,x,y,z)
      sym_ops = [n*'x,y,z'] array of string symmetry operations
      x,y,z = fractional coordinates of atomic posiiton to be modified by symmetry
      uvw = [[nx3]] array of symmetry defined factional coordinates [u,v,w]

    E.G.
      uvw = gen_sym_pos(['x,y,z','y,-x,z+1/2'],0.1,0.2,0.3)
      uvw >> [[0.1,0.2,0.3] , [0.2,-0.1,0.8]]
    """
    uvw = np.zeros([len(sym_ops), 3])
    for n in range(len(sym_ops)):
        sym = sym_ops[n]
        sym = sym.lower()
        # Evaluate string symmetry operation in terms of x,y,z
        sym = sym.replace('/', './')
        sym = sym.strip('\"\'')
        out = eval(sym)
        uvw[n] = np.array(out[0:3]) + 0.0  # add zero to remove -0.0 values
    return uvw


def gen_symcen_pos(sym_ops, cen_ops, x, y, z):
    """
    Generate positions from symmetry and centring operations
    Usage:
      uvw = gen_symcen_pos(sym_ops,cen_ops,x,y,z)
      sym_ops = [n*'x,y,z'] array of string symmetry operations
      cen_ops = [m*'x,y,z'] array of string centring operations
      x,y,z = fractional coordinates of atomic posiiton to be modified by symmetry
      uvw = [[nx3]] array of symmetry defined factional coordinates [u,v,w]

    E.G.
      uvw = gen_symcen_pos(['x,y,z','y,-x,z+1/2'],['x,y,z','x+1/3,y+1/3,z'],0.1,0.2,0.3)
      uvw >> [[0.1,0.2,0.3] , [0.433,0.533,0.3] , [0.2,-0.1,0.8] , [0.533,-0.233,0.8]]
    """

    NsymOps = len(sym_ops)
    NcenOps = len(cen_ops)
    Nops = NsymOps * NcenOps

    uvw = gen_sym_pos(sym_ops, x, y, z)

    sympos = np.zeros([Nops, 3])
    for m in range(NsymOps):
        cx, cy, cz = uvw[m]
        Ni, Nj = m * NcenOps, (m + 1) * NcenOps
        cen_uvw = gen_sym_pos(cen_ops, cx, cy, cz)
        sympos[Ni:Nj, :] = cen_uvw
    return sympos


def gen_symcen_ops(sym_ops, cen_ops):
    """
    Build complete list of symmetry operations from symmetry and centring vectors
    Usage:
      ops = gen_symcen_ops(sym_ops,cen_ops)
      sym_ops = [n*'x,y,z'] array of string symmetry operations
      cen_ops = [m*'x,y,z'] array of string centring operations
      ops = [n*m*'x,y,z'] array of string symmetry operations

    E.G.
      ops = gen_symcen_pos(['x,y,z','y,-x,z+1/2'],['x,y,z','x+1/3,y+1/3,z'])
      >> ops = ['x,y,z','x+1/3,y+1/3,z','y,-x,z+1/2','y+1/3,-x+1/3,z+1/2']
    """

    ops = []
    for sym in sym_ops:
        sym = sym.lower()
        sym = sym.strip('\"\'')
        x, y, z = sym.split(',')
        x = x.strip()
        y = y.strip()
        z = z.strip()
        for cen in cen_ops:
            cen = cen.lower()
            cen = cen.strip('\"\'')
            op = cen.replace('x', 'a').replace('y', 'b').replace('z', 'c')  # avoid replacing x/y twice
            op = op.replace('a', x).replace('b', y).replace('c', z)
            op = op.replace('--', '')
            ops += [op]
    return ops


def gen_sym_ref(sym_ops, hkl):
    """
     Generate symmetric reflections given symmetry operations
         symhkl = gen_sym_ref(sym_ops,h,k,l)
    """

    hkl = np.asarray(hkl, dtype=np.float)

    # Get transformation matrices
    sym_mat = gen_sym_mat(sym_ops)
    nops = len(sym_ops)

    symhkl = np.zeros([nops, 4])
    for n, sym in enumerate(sym_mat):
        symhkl[n, :] = np.dot(hkl, sym)

    return symhkl[:, :3]


def sum_sym_ref(symhkl):
    """
    Remove equivalent hkl positions and return the number of times each is generated.
    """
    # Remove duplicate positions
    uniquehkl, uniqueidx, matchidx = fg.unique_vector(symhkl[:, :3], 0.01)

    # Sum intensity at duplicate positions
    sumint = np.zeros(len(uniquehkl))
    for n in range(len(uniquehkl)):
        sumint[n] = matchidx.count(n)

    return uniquehkl, sumint


def gen_sym_mat(sym_ops):
    """
     Generate transformation matrix from symmetry operation
     Currently very ugly but it seems to work
     sym_mat = gen_syn_mat(['x,y,z','y,-x,z+1/2'])
     sym_mat[0] = [[ 1.,  0.,  0.,  0.],
                   [ 0.,  1.,  0.,  0.],
                   [ 0.,  0.,  1.,  0.]])
     sym_mat[1] = [[ 0. ,  1. ,  0. ,  0. ],
                   [-1. ,  0. ,  0. ,  0. ],
                   [ 0. ,  0. ,  1. ,  0.5]]
    """
    sym_mat = []
    for sym in sym_ops:
        sym = sym.lower()
        ops = sym.split(',')
        mat = np.zeros([3, 4])

        for n in range(len(ops)):
            op = ops[n]
            op = op.strip('\"\'')
            if 'x' in op: mat[n, 0] = 1
            if '-x' in op: mat[n, 0] = -1
            if 'y' in op: mat[n, 1] = 1
            if '-y' in op: mat[n, 1] = -1
            if 'z' in op: mat[n, 2] = 1
            if '-z' in op: mat[n, 2] = -1

            # remove these parts
            op = op.replace('-x', '').replace('x', '')
            op = op.replace('-y', '').replace('y', '')
            op = op.replace('-z', '').replace('z', '')
            op = op.replace('+', '')
            op = op.replace('/', './')  # Allow float division

            if len(op.strip()) > 0:
                mat[n, 3] = eval(op)
        sym_mat += [mat]
    return sym_mat


def invert_sym(sym_op):
    """
    Invert the sign of the given symmetry operation
    Usage:
      new_op = invert_sym(sym_op)
      sym_op = str symmetry operation e.g. 'x,y,z'
      new_op = inverted symmetry
    E.G.
      new_op = invert_sym('x,y,z')
      >> new_op = '-x,-y,-z'
    """
    sym_op = sym_op.lower()
    new_op = sym_op.replace('x', '-x').replace('y', '-y').replace('z', '-z').replace('--', '+').replace('+-', '-')
    return new_op


def orthogonal_axes(x_axis=[1, 0, 0], y_axis=[0, 1, 0]):
    """
    Returns orthogonal right-handed cartesian axes based on the plane of two non-perpendicular vectors
    E.G.
        x,y,z = orthogonal_axes([1,0,0],[0.5,0.5,0])
        >> x = array([1,0,0])
        >> y = array([0,1,0])
        >> z = array([0,0,1])
    E.G.
        x,y,z = orthogonal_axes([0,1,0],[0,0,1])
        >> x = array([0,1,0])
        >> y = array([0,0,1])
        >> z = array([1,0,0])
    """

    x_cart = fg.norm(x_axis)
    y_cart = fg.norm(y_axis)
    z_cart = fg.norm(np.cross(x_cart, y_cart))  # z is perp. to x+y
    y_cart = np.cross(x_cart, z_cart)  # make sure y is perp. to x
    return x_cart, y_cart, z_cart


'----------------------------Conversions-------------------------------'


def latpar2UV(a, b, c, alpha=90., beta=90., gamma=120.):
    """
    Convert a,b,c,alpha,beta,gamma to UV
     UV = latpar2UV(a,b,c,alpha=90.,beta=90.,gamma=120.)
     Vector c is defined along [0,0,1]
     Vector a and b are defined by the angles
    """

    # From http://pymatgen.org/_modules/pymatgen/core/lattice.html
    alpha_r = np.radians(alpha)
    beta_r = np.radians(beta)
    gamma_r = np.radians(gamma)
    val = (np.cos(alpha_r) * np.cos(beta_r) - np.cos(gamma_r)) \
          / (np.sin(alpha_r) * np.sin(beta_r))
    # Sometimes rounding errors result in values slightly > 1.
    val = abs(val)
    gamma_star = np.arccos(val)
    aa = [a * np.sin(beta_r), 0.0, a * np.cos(beta_r)]
    bb = [-b * np.sin(alpha_r) * np.cos(gamma_star),
          b * np.sin(alpha_r) * np.sin(gamma_star),
          b * np.cos(alpha_r)]
    cc = [0.0, 0.0, c]

    return np.round(np.array([aa, bb, cc]), 8)


def latpar2UV_rot(a, b, c, alpha=90., beta=90., gamma=120.):
    """
    Convert a,b,c,alpha,beta,gamma to UV
     UV = latpar2UV_rot(a,b,c,alpha=90.,beta=90.,gamma=120.)
     Vector b is defined along [0,1,0]
     Vector a and c are defined by the angles
    """

    # From http://pymatgen.org/_modules/pymatgen/core/lattice.html
    alpha_r = np.radians(alpha)
    beta_r = np.radians(gamma)
    gamma_r = np.radians(beta)
    val = (np.cos(alpha_r) * np.cos(beta_r) - np.cos(gamma_r)) \
          / (np.sin(alpha_r) * np.sin(beta_r))
    # Sometimes rounding errors result in values slightly > 1.
    val = abs(val)
    gamma_star = np.arccos(val)
    aa = [a * np.sin(beta_r), a * np.cos(beta_r), 0.0]
    bb = [0.0, b, 0.0]
    cc = [-c * np.sin(alpha_r) * np.cos(gamma_star),
          c * np.cos(alpha_r),
          c * np.sin(alpha_r) * np.sin(gamma_star)]

    return np.round(np.array([aa, bb, cc]), 8)


def UV2latpar(UV):
    """
    Convert UV=[a,b,c] to a,b,c,alpha,beta,gamma
     a,b,c,alpha,beta,gamma = UV2latpar(UV)
    """

    a = np.sqrt(np.sum(UV[0] ** 2))
    b = np.sqrt(np.sum(UV[1] ** 2))
    c = np.sqrt(np.sum(UV[2] ** 2))
    alpha = np.arctan2(np.linalg.norm(np.cross(UV[1], UV[2])), np.dot(UV[1], UV[2])) * 180 / np.pi
    beta = np.arctan2(np.linalg.norm(np.cross(UV[0], UV[2])), np.dot(UV[0], UV[2])) * 180 / np.pi
    gamma = np.arctan2(np.linalg.norm(np.cross(UV[0], UV[1])), np.dot(UV[0], UV[1])) * 180 / np.pi
    return a, b, c, alpha, beta, gamma


def hkl2Q(hkl, UVstar):
    """
    Convert reflection indices (hkl) to orthogonal basis in A-1
    :param hkl: [nx3] array of reflections
    :param UV: [3x3] array of unit cell vectors [[a1,a2,a3],[b1,b2,b3],[c1,c2,c3]]
    :return: [nx3] array of wavevectors in an orthogonal basis, in A-1
    """
    return np.dot(hkl, UVstar)


def Q2hkl(qvec, UVstar):
    """
    Index vectors in an orthonal basis with a reciprocal basis
    :param qvec: [nx3] array of coordinates in an orthogonal basis in A-1
    :param UV: [3x3] array of unit cell vectors [[a1,a2,a3],[b1,b2,b3],[c1,c2,c3]]
    :return: [nx3] array of vectors in reciprocal lattice units
    """
    return fg.index_coordinates(qvec, UVstar)


def hkl2Qmag(hkl, UVstar):
    """
    Calcualte magnitude of Q from hkl reflection
    :param hkl: [nx3] array of reflections
    :param UV: [3x3] array of unit cell vectors
    :return: [nx1] array of wavevector magnitudes, in A-1
    """
    Q = np.dot(hkl, UVstar)
    return fg.mag(Q)


def hkl2dspace(hkl, UVstar):
    """
    Calcualte d-spacing from hkl reflection
    :param hkl: [nx3] array of reflections
    :param UV: [3x3] array of unit cell vectors
    :return: [nx1] array of d-spacing in A
    """
    Q = np.dot(hkl, UVstar)
    Qmag = fg.mag(Q)
    return q2dspace(Qmag)


def calqmag(twotheta, energy_kev=17.794):
    """
    Calculate |Q| at a particular 2-theta (deg) for energy in keV
     magQ = calqmag(twotheta, energy_kev=17.794)
    """

    energy = energy_kev * 1000.0  # energy in eV
    theta = twotheta * np.pi / 360  # theta in radians
    # Calculate |Q|
    magq = np.sin(theta) * energy * fg.e * 4 * np.pi / (fg.h * fg.c * 1e10)
    return magq


def cal2theta(qmag, energy_kev=17.794):
    """
    Calculate theta at particular energy in keV from |Q|
     twotheta = cal2theta(Qmag,energy_kev=17.794)
    """

    energy = energy_kev * 1000.0  # energy in eV
    # Calculate 2theta angles for x-rays
    twotheta = 2 * np.arcsin(qmag * 1e10 * fg.h * fg.c / (energy * fg.e * 4 * np.pi))
    # return x2T in degrees
    twotheta = twotheta * 180 / np.pi
    return twotheta


def caldspace(twotheta, energy_kev=17.794):
    """
    Calculate d-spacing from two-theta
     dspace = caldspace(tth, energy_kev)
    """
    qmag = calqmag(twotheta, energy_kev)
    dspace = q2dspace(qmag)
    return dspace


def q2dspace(qmag):
    """
    Calculate d-spacing from |Q|
         dspace = q2dspace(Qmag)
    """
    return 2 * np.pi / qmag


def dspace2q(dspace):
    """
    Calculate d-spacing from |Q|
         Qmag = q2dspace(dspace)
    """
    return 2 * np.pi / dspace


def wave2energy(wavelength):
    """
    Converts wavelength in A to energy in keV
     Energy = wave2energy(wavelength)
    """

    # SI: E = hc/lambda
    lam = wavelength * fg.A
    E = fg.h * fg.c / lam

    # Electron Volts:
    Energy = E / fg.e
    return Energy / 1000.0


def energy2wave(energy_kev):
    """
    Converts energy in keV to wavelength in A
     wavelength = energy2wave(energy)
    """

    # Electron Volts:
    E = 1000 * energy_kev * fg.e

    # SI: E = hc/lambda
    lam = fg.h * fg.c / E
    wavelength = lam / fg.A
    return wavelength


def biso2uiso(biso):
    """
    Convert B isotropic thermal parameters to U isotropic thermal parameters
    :param biso: Biso value or array
    :return: Uiso value or array
    """
    biso = np.asarray(biso, dtype=np.float)
    return biso / (8 * np.pi ** 2)


def uiso2biso(uiso):
    """
    Convert U isotropic thermal parameters to B isotropic thermal parameters
    :param uiso: Uiso value or array
    :return: Biso value or array
    """
    uiso = np.asarray(uiso, dtype=np.float)
    return uiso * (8 * np.pi ** 2)


def diffractometer_Q(eta, delta, energy_kev=8.0):
    """
    Calculate wavevector transfer, Q for diffractometer within the scattering plane.
       Qx,Qy = diffractometer_Q(eta,delta,energy_kev)
       eta = angle (deg) of sample
       delta = angle (deg) of detector
       energy_kev = energy in keV

       Coordinate system (right handed):
        x - direction along beam, +ve is from source to sample
        y - direction verticle
        z - direction horizontal

       Note: Currently only in the verticle geometry!
    """

    delta = np.radians(delta)
    eta = np.radians(eta)
    K = 1E-10 * 1000 * 2 * np.pi * (energy_kev * fg.e) / (fg.h * fg.c)  # K vector magnitude

    Qx = K * (np.cos(eta) - np.cos(delta - eta))
    Qy = K * (np.sin(delta - eta) + np.sin(eta))
    return Qx, Qy


def symmetry_ops2magnetic(operations):
    """
    Convert list of string symmetry operations to magnetic symmetry operations
    i.e. remove translations
    """
    # convert string to list
    if type(operations) is str:
        operations = [operations]

    rem = ['+1/2', '+1/3', '+2/3', '+1/6', '+5/6']
    return [fg.multi_replace(sp, rem, '') for sp in operations]


def hkl2str(hkl):
    """
    Convert hkl to string (h,k,l)
    :param hkl:
    :return: str '(h,k,l)'
    """

    out = '(%1.3g,%1.3g,%1.3g)'
    hkl = np.asarray(hkl, dtype=np.float).reshape([-1, 3])
    hkl = np.around(hkl, 5)
    return '\n'.join([out % (x[0], x[1], x[2]) for x in hkl])


def cut2powder(qx, qy, qz, cut):
    """
    Convert 2D reciprocal space cut to powder pattern
    :param qx: [n,m] array of Q coordinates in x
    :param qy: [n,m] array of Q coordinates in y
    :param qz: [n,m] array or float of Q coordinates in z
    :param cut: [n,m] array of intensities
    :return: qm[o], pow[o]
    """
    qq = np.sqrt(qx**2 + qy**2 + qz**2)
    return fg.grid_intensity(qq.ravel(), cut.ravel())


'--------------------------Misc Crystal Programs------------------------'


def powder_average(tth, energy_kev):
    """
    Return the powder average correction for intensities at a given two-theta
        Ip = I0*PA,    PA = 1/|Q|^2
    :param tth: two-theta in deg
    :param energy_kev: energy in keV
    :return: PA
    """
    q = calqmag(tth, energy_kev)
    return 1/q**2


def calc_vol(UV):
    "Calculate volume in Angstrom^3 from unit vectors"
    a, b, c = UV
    return np.dot(a, np.cross(b, c))


def cif2table(cif):
    """
    Generate Latex table of atomic positions from cif dictionary
    :param cif: cif dict from readcif
    :return: str
    """

    keys = cif.keys()

    # Generate unit vectors
    a = cif['_cell_length_a']
    b = cif['_cell_length_b']
    c = cif['_cell_length_c']
    alpha = cif['_cell_angle_alpha']
    beta = cif['_cell_angle_beta']
    gamma = cif['_cell_angle_gamma']
    lp = r'a=%s\AA, b=%s\AA, c=%s\AA, $\alpha$=%s, $\beta$=%s, $\gamma$=%s' % (a, b, c, alpha, beta, gamma)

    # Get atom names & labels
    label = cif['_atom_site_label']

    # Thermal parameters
    if '_atom_site_U_iso_or_equiv' in keys:
        u_or_b = 'U$_{iso}$'
        uiso = cif['_atom_site_U_iso_or_equiv']
    elif '_atom_site_B_iso_or_equiv' in keys:
        u_or_b = 'B$_{iso}$'
        uiso = cif['_atom_site_B_iso_or_equiv']
    else:
        u_or_b = 'U$_{iso}$'
        uiso = ['0.000']*len(label)
    # Occupancy
    if '_atom_site_occupancy' in keys:
        occ = cif['_atom_site_occupancy']
    else:
        occ = ['1.0']*len(label)
    # Multiplicity
    if '_atom_site_site_symmetry_multiplicity' in keys:
        mult = [s+'a' for s in cif['_atom_site_site_symmetry_multiplicity']]
    else:
        mult = ['1a']*len(label)

    # Get coordinates
    u = cif['_atom_site_fract_x']
    v = cif['_atom_site_fract_y']
    w = cif['_atom_site_fract_z']

    # Get space group
    if '_symmetry_space_group_name_H-M' in keys:
        spacegroup = cif['_symmetry_space_group_name_H-M']
    elif '_space_group_name_H-M_alt' in keys:
        spacegroup = cif['_space_group_name_H-M_alt']
    else:
        spacegroup = ''
    if '_symmetry_Int_Tables_number' in keys:
        sgn = float(cif['_symmetry_Int_Tables_number'])
    elif '_space_group_IT_number' in keys:
        sgn = float(cif['_space_group_IT_number'])
    elif spacegroup == 'P1':
        sgn = 1
    else:
        sgn = 0

    # Aditional details:
    if 'FileTitle' in keys:
        name = cif['FileTitle']
    else:
        name = 'sample'

    extra = []
    if '_cell_measurement_temperature' in keys:
        extra += ['T = %s' % cif['_cell_measurement_temperature']]
    if '_diffrn_reflns_number' in keys:
        extra += ['%s reflections' % cif['_diffrn_reflns_number']]
    if '_refine_ls_wR_factor_ref' in keys:
        extra += ['R$_w$ = %4.2f\\%%' % (float(cif['_refine_ls_wR_factor_ref'])*100)]
    extra = ', '.join(extra)

    # Create table str
    out = '%% %s\n' % cif['Filename']
    out += '\\begin{table}[htp]\n'
    out += '    \\centering\n'
    out += '       \\begin{tabular}{c|c|ccccc}\n'
    out += '             & Site & x & y & z & Occ. & %s \\\\ \hline\n' % u_or_b
    fmt = '        %4s & %5s & %s & %s & %s & %s & %s \\\\\n'
    for n in range(len(label)):
        out += fmt % (label[n], mult[n], u[n], v[n], w[n], occ[n], uiso[n])
    out += '        \\end{tabular}\n'
    out += '    \\caption{%s with %s. %s}\n' % (name, lp, extra)
    out += '    \\label{tab:}\n'
    out += '\\end{table}\n'
    return out