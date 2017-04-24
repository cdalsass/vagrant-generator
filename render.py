import jinja2
from jinja2 import meta
import yaml
import os

class render(object):

    data = ''
    render_template = ''

    def __init__(self, data_file, template_file):
        #read yaml file
        try:
            with open(data_file) as read_data:
                self.data = yaml.load(read_data)
            read_data.close()
        except IOError:
            print "can't open yaml file {}".format(data_file)
        #check for data file
        self.render_template = template_file
        if not os.path.exists(self.render_template):
            raise IOError("Template file {} cannot be opened".format(template_file))

    def load_template_from_file(self):
        templateloader = jinja2.FileSystemLoader(searchpath="./")
        templateenv = jinja2.Environment(loader=templateloader)
        return templateenv.get_template(self.render_template)

    def to_stdout(self):
        """Render template to stdout """
        my_template = self.load_template_from_file()
        return my_template.render(self.data)

    def to_file(self, filename, verbose='no'):
        """Render template to file"""
        my_template = self.load_template_from_file()
        if os.path.exists(filename):
            overwrite_file = raw_input('The file already exists. Do you wish to overwrite (Y/N)?')
            if overwrite_file.upper() == 'Y':
                print "backing up {} to {}.backup".format(filename,filename)
                file_backup = filename + ".backup"
                try:
                    with open(file_backup, mode='w') as backup:
                        with open(filename, mode='r') as backup_src:
                            backup.write(backup_src.read())
                    backup.close()
                    backup_src.close()
                except IOError as e:
                    print "unable to backup... {}".format(e)
                    exit()
                print "overwriting file {}...".format(filename)

            else:
                print "not overwriting file {}".format(filename)
                exit()
        try:
            with open(filename, mode='w') as outputfile:
                outputfile.write(my_template.render(self.data))
            outputfile.close()
            if verbose == 'yes':
                print "Writing the following to {}".format(filename)
                print '****************************'
                print self.to_stdout()
        except IOError as e:
            print "Unable to write to file {}: {}".format(filename,e)
        def show_values(self):
            return yaml.dump(self.data)

    def list_template_vars(self):
        validateloader = jinja2.FileSystemLoader(searchpath="./")
        validate_env = jinja2.Environment(loader=validateloader)
        validate_source = open(self.render_template)
        validate_ast = validate_env.parse(validate_source.read())
        return sorted(list(jinja2.meta.find_undeclared_variables(validate_ast)))

    def list_data_vars(self):
        return sorted([x for x in self.data.keys()])

    def validate(self):
        template_vars = self.list_template_vars()
        data_vars   = self.list_data_vars()
        return template_vars == data_vars


if __name__ == '__main__':
    yaml_file = 'test.yaml'
    template = 'test.tpl'
    make_file = render(yaml_file, template)
    make_file.to_file('testrender.txt', verbose='yes')

