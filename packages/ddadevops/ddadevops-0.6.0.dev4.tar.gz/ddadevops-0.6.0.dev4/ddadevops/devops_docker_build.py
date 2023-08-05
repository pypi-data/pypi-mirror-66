from subprocess import run
from .python_util import filter_none
from pkg_resources import *
from .devops_terraform_build import DevopsBuild, create_devops_build_config


def create_devops_docker_build_config(stage,
                                      project_root_path,
                                      module,
                                      build_dir_name='target',
                                      use_package_common_files=True,
                                      build_commons_path=None,
                                      docker_build_commons_dir_name='docker',):
    ret = create_devops_build_config(
        stage, project_root_path, module, build_dir_name)
    ret.update({'use_package_common_files': use_package_common_files,
                'build_commons_path': build_commons_path,})
    return ret


class DevopsDockerBuild(DevopsBuild):

    def __init__(self, project, config):
        super().__init__(project, config)
        project.build_depends_on('python-terraform')
        self.use_package_common_files = config['use_package_common_files']
        self.build_commons_path = config['build_commons_path']
        self.docker_build_commons_dir_name = config['docker_build_commons_dir_name']
        

    def docker_build_commons_path(self):
        mylist = [self.build_commons_path,
                  self.docker_build_commons_dir_name]
        return '/'.join(filter_none(mylist)) + '/'

    def copy_build_resource_file_from_package(self, name):
        my_data = resource_string(
            __name__, "src/main/resources/docker/" + name)
        with open(self.build_path() + '/' + name, "w") as output_file:
            output_file.write(my_data.decode(sys.stdout.encoding))

    def copy_build_resources_from_package(self):
        self.copy_build_resource_file_from_package('image/resources/install_functions.sh')

    def copy_build_resources_from_dir(self):
        run('cp -f ' + self.docker_build_commons_path() +
            '* ' + self.build_path(), shell=True)

    def initialize_build_dir(self):
        super().initialize_build_dir()
        if self.use_package_common_files:
            self.copy_build_resources_from_package()
        else:
            self.copy_build_resources_from_dir()
        run('cp -r image ' + self.build_path(), shell=True)
        run('cp -r test ' + self.build_path(), shell=True)