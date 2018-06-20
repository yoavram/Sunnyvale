# import tempfile
import shutil
import os.path
from os.path import join as join_path
from os.path import split as split_path
import re
from zipfile import ZipFile

if __name__ == '__main__':
	ms_dir = '.'
	figures_dir = '../figures'
	ms_figures_dir = join_path(ms_dir, 'figures')
	zip_fname = '/Users/yoavram/Dropbox/Sunnyvale/figures.zip'
	tex_files = ['ms_sunnyvale.tex']
	pattern = re.compile(r'\\includegraphics(?:\[.*\])?\{(.*\.\w{3})\}')

	if os.path.exists(ms_figures_dir):
		shutil.rmtree(ms_figures_dir)
		os.mkdir(ms_figures_dir)
	if not os.path.exists(ms_figures_dir):
		os.mkdir(ms_figures_dir)

	figures = []
	for fn in tex_files:
		with open(join_path(ms_dir, fn)) as f:
			matches = (pattern.match(line) for line in f)
			matches = (m for m in matches if m is not None)
			filenames = (m.groups()[0] for m in matches)
			filenames = (split_path(fn)[-1] for fn in filenames)
			filenames = (join_path(figures_dir, fn) for fn in filenames)
			figures.extend(filenames)

	with ZipFile(zip_fname, 'w') as z:
		for fn in figures:
			fn = fn.replace('{', '').replace('}', '')
			print(fn)
			shutil.copy(fn, join_path(ms_figures_dir, split_path(fn)[-1]))
			z.write(fn)

	print("{} figures copied to {} and zipped to {}".format(
		len(figures), ms_figures_dir, zip_fname))
