# LICENSE: MIT
# Copyright 2020: Michael DeHaan <michael@michaeldehaan.net>

import os
import jinja2
import importlib
import glob

from . import snippets

class Builder(object):
	
	def __init__(self, input_path=None, output_path=None, variables=None, theme=None,
	             upload_method=None, sections=None, index=None, page_title_template=None,
	             theme_options=None):
		
		assert input_path is not None
		assert output_path is not None
		assert theme is not None
		assert input_path != output_path
		assert index is not None
		assert sections is not None
		assert page_title_template is not None
		
		self.input_path = input_path
		self.output_path = output_path
		
		assert 'output' in self.output_path
		
		self.theme = theme
		self.upload_method = upload_method
		self.index = index
		self.sections = sections
		self.page_title_template = page_title_template
		

		if theme_options is None:
			theme_options = dict()
		if variables is None:
			variables = dict()
			
		merged_variables = dict()
		merged_variables.update(theme_options)
		merged_variables.update(variables)
		
		self.variables = merged_variables
		self.theme_options = theme_options
		
		self.import_theme(theme)
		self.init_jinja2()
	
	def import_theme(self, theme):
		
		self.theme = importlib.import_module(theme)
	
	def build(self):
		
		self.destroy_output_directory()
		self.create_output_directory()
		self.load_block_snippets()
		self.build_title_map()
		self.copy_theme_files()
		self.render_pages_to_disk()
		self.cleanup_output_directory()
		
	def init_jinja2(self):
		
		self.loader = jinja2.FileSystemLoader(searchpath="/")
		self.jenv_strict = jinja2.Environment(loader=self.loader, undefined=jinja2.StrictUndefined)
		
	def load_block_snippets(self):
		
		# block snippets are pieces of themes that can be overriden in the local project directory
		# examples: footer.j2, header.j2
		
		for x in self.theme.SNIPPETS:
			self.load_block_snippet(x)
			
	def probe_file_location(self, name):
		
		snippet_file = self.snippet_path("%s.j2" % name)
		theme_file = self.theme_path("%s.j2" % name)
		input_file = os.path.join(self.input_path, "%s.j2" % name)
		
		use_file = snippet_file
		
		if os.path.exists(theme_file):
			use_file = theme_file
		if os.path.exists(input_file):
			use_file = input_file
		return use_file
		
	def load_block_snippet(self, snippet_name):

		use_file = self.probe_file_location(snippet_name)
		data = open(use_file).read()
		string_env = jinja2.Environment(loader=jinja2.BaseLoader).from_string(data)
		self.variables['SNIPPET_%s' % snippet_name] = string_env.render(self.variables)
		

	def render_html_template_to_disk(self, section_name, page_name, input_filename):
		
		output_filename = self.get_output_filename(input_filename)
		
		string_env = jinja2.Environment(loader=jinja2.BaseLoader)
		string_env = string_env.from_string(self.page_title_template)
		
		self.variables['ROCKCHISEL_active_section'] = section_name
		self.variables['title'] = page_name
		self.variables['ROCKCHISEL_page_title'] = string_env.render(self.variables)
		
		variables = self.compute_variables_for_theme_template(input_filename)
		
		print("* writing: %s" % output_filename)
		assert 'output' in output_filename
		output_file = open(output_filename, 'w')
		theme_file = self.theme_path('theme.j2')
		theme_template = self.jenv_strict.get_template(theme_file)
		page_data = theme_template.render(variables)
		output_file.write(page_data)
		output_file.close()
		
	def create_output_directory(self):
		if not os.path.exists(self.output_path):
			os.mkdir(self.output_path)
		
	def render_css_template_to_disk(self, input_filename):
		
		output_filename = self.get_output_filename(input_filename)
		print("* writing: %s" % output_filename)
		css_template = self.jenv_strict.get_template(input_filename)
		page_data = css_template.render(self.theme_options)
		output_file = open(output_filename, 'w')
		output_file.write(page_data)
		output_file.close()

		
	def theme_path(self, file=None):
		base = os.path.join(os.path.dirname(os.path.abspath(self.theme.__file__)))
		if file is None:
			return base
		return os.path.join(base, file)
		
	def snippet_path(self, file=None):
		base = os.path.join(os.path.dirname(os.path.abspath(snippets.__file__)))
		if file is None:
			return base
		return os.path.join(base, file)
		
	def build_title_map(self):
		map = {}
		for (section_name, v) in self.sections.items():
			for (page_name, template_name) in v.items():
				map[template_name] = page_name
		self.variables['ROCKCHISEL_title_map'] = map
		
	def render_pages_to_disk(self):
		
		# HTML
		for (section_name, v) in self.sections.items():
			print("* section: %s" % section_name)
			for (page_name, template_name) in v.items():
				print("* page: %s" % page_name)
				input_filename = os.path.join(self.input_path, "%s.j2" % template_name)
				print("* input: %s" % input_filename)
				self.render_html_template_to_disk(section_name, page_name, input_filename)
				
		# CSS (from theme)
		theme_dir = self.theme_path()
		css_templates = glob.glob(os.path.join(self.theme_path(), "*.css"))
		for f in css_templates:
			self.render_css_template_to_disk(f)
	
	def get_output_filename(self, input_filename):
		
		base = os.path.basename(input_filename)
		if '.j2' in input_filename:
			base = base.replace('.j2', '.html')
		result = os.path.join(self.output_path, base)
		return result
	
	def copy_theme_files(self):
		print("* copying theme files")
		os.system("cp -r %s/* %s" % (self.theme_path, self.output_path))
		
	def destroy_output_directory(self):
		print("* erasing output directory")
		
		# avoid accidental deletion of an important directory
		assert 'output' in self.output_path
		
		# delete all previous files
		os.system("rm -rf %s" % self.output_path)
	
	def cleanup_output_directory(self):
		
		# avoid accidental deletion from an important directory
		assert 'output' in self.output_path
		
		# prevent accidental upload of jinja2 and python files
		# we only do this because the cp -r in copy_theme_files doesn't have an allow list (yet)
		os.system("rm -rf %s/*.j2" % self.output_path)
		os.system("rm -rf %s/*.py" % self.output_path)
		
	def render_template_as_string(self, input_filename, variables):
		
		input_filename = os.path.abspath(input_filename)
		
		macro_data = ""
		
		# we have to prepend the macro templates so they'll actually run
		for macro in self.theme.MACROS:
			file_path = self.probe_file_location(macro)
			macro_data = macro_data + open(file_path).read() + "\n"
			
		template_data = open(input_filename).read()
		template_data = macro_data + "\n" + template_data
		
		content_template = self.jenv_strict.from_string(template_data)
		
		return content_template.render(variables)
	
	def compute_variables_for_theme_template(self, input_filename):
		variables = self.variables.copy()
		variables.update(self.theme.VARIABLES)
		variables['ROCKCHISEL_sections'] = self.sections
		variables['ROCKCHISEL_page_content'] = self.render_template_as_string(input_filename, variables)
		return variables
		





