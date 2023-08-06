#!python

import os
import sys
import argparse
import numpy as np 
import datatable as dt
import magicBatch

class ArgumentParserError(Exception):
	pass

class NewArgumentParser(argparse.ArgumentParser):
	def error(self, message):
		print(message)
		sys.exit(0)


def parse_args(args):
	p = NewArgumentParser(description='run MAGIC')
	a = p.add_argument_group('data loading parameters')
	a.add_argument('-d', '--data_file', metavar='D',
					help='File path of input data file.')
	a.add_argument('-a', '--aff_mat_input_data_file', metavar='A', 
					help='File path of affinity matrix input data file.')
	a.add_argument('-o', '--output_file', metavar='O', required=True,
				   help='File path of where to save the MAGIC imputed data (in csv format).')
	a.add_argument('-q', '--output_file2', metavar='Q', required=True,
				   help='File path of where to save the diffusion map data (in csv format).')

	m = p.add_argument_group('MAGIC parameters')
	m.add_argument('-p', '--pca-components', metavar='P', default=20, type=int,
				   help='Number of pca components to use when running MAGIC (Default = 20).')
	m.add_argument('--pca-non-random', default=True, action='store_false',
				    help='Do not used randomized solver in PCA computation.')
	m.add_argument('-k', metavar='K', default=9, type=int,
					help='Number of nearest neighbors to use when running MAGIC (Default = 9).')
	m.add_argument('-ka', metavar='KA', default=3, type=int,
					help='knn-autotune parameter for running MAGIC (Default = 3).')
	m.add_argument('-e', '--epsilon', metavar='E', default=1, type=int,
					help='Epsilon parameter for running MAGIC (Default = 1).')

	w = p.add_argument_group('Diffusion Map parameters')
	w.add_argument('-c', '--n_diffusion_components', metavar='C', default=10, type=int,
					help='Number of diffusion map components to calculate (Default = 10).')

	try:
		return p.parse_args(args)
	except ArgumentParserError:
		raise


def main(args: list = None):
	args = parse_args(args)
	print(args)
	try:
		if args.aff_mat_input_data_file != None:
			aff_mat_input_data = dt.fread(args.aff_mat_input_data_file)
		
			#aff_mat_input_data.set_index(list(aff_mat_input_data.columns[[0]]), inplace=True)
				
			magic.MAGIC_core.magic(aff_mat_input = aff_mat_input_data, n_pca_components=args.pca_components, random_pca=args.pca_non_random, k=args.k, ka=args.ka, epsilon=args.epsilon, n_diffusion_components=args.n_diffusion_components, csv_l=args.output_file, csv_d=args.output_file2)
		else: 
			dat_norm = dt.fread(args.data_file)
			magic.MAGIC_core.magic(data=dat_norm, n_pca_components=args.pca_components, random_pca=args.pca_non_random, k=args.k, ka=args.ka, epsilon=args.epsilon, n_diffusion_components=args.n_diffusion_components, csv_l=args.output_file, csv_d=args.output_file2)

		
		
		
	except:
		raise

if __name__ == '__main__':
	main(sys.argv[1:])
