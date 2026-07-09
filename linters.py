import yamllint.config
import yamllint.linter
from pathlib import Path
import re


class YamlLinter:
    yamls=['yaml/gui.yaml','yaml/print.yaml']
    log_path = Path('./logs/linter.log')
    log_path.parent.mkdir(parents=True, exist_ok=True)

    def lint_files(self):
        'Functions for linting yamls'
        
        yaml_config = yamllint.config.YamlLintConfig(content="extends: default")
        
        self.log_path.write_text('\n')
        for file in self.yamls:
            error_count = 0
            
            yaml_path = Path(file)
            cwd = Path.cwd()
            yaml_path.parent.mkdir(parents=True, exist_ok=True)
            self.log_path.write_text(self.log_path.read_text()+'Report of Linter for '+file+':\n')
            for p in yamllint.linter.run(yaml_path.open(mode='r', encoding='UTF-8'), yaml_config):
                if (p):
                    error_count += 1
                self.log_path.write_text(self.log_path.read_text()+str(p.level)+' at line '+str(p.line)+': '+p.desc+'\n')
        return error_count
    
    def analyze_syntax(self):
        'Function for analyzing content of yamls'
        for file in self.yamls:
            error_count=0
            yaml_path = Path(file)
            yaml_path.open(mode='r')
            strings=yaml_path.read_text().splitlines()
            if (file == self.yamls[0]):
                self.log_path.write_text(self.log_path.read_text()+'Analyzing ' + self.yamls[0] +' file\n')
                error_count=self.analyze_gui(strings)
            if (file == self.yamls[1]):
                self.log_path.write_text(self.log_path.read_text()+'Analyzing ' + self.yamls[1] +' file\n')
        return error_count
    
    def analyze_gui(self,strings):
        '''Analyze gui yaml'''
        error_count=0
        string_num=1 #like yamllint
        pattern_s=r'type|id|label|content|orient|values'
        pattern_i=r"pos_x|pos_y|height|width|value|length"
        pattern_f=r"variable|from|to|resolution|increment"
        for string in strings:
            if (string.strip(' ') == '---' or string.strip(' ') == '-' or string.strip(' ') == 'content:'):
                string_num += 1
                continue
            result=string.strip(' ').rsplit(': ')
            if (len(result) != 2):
                error_count += 1
                self.log_path.write_text (self.log_path.read_text()+"Error in line " + str(string_num)+ " - every string in yaml file should be a <parameter>: <value>\n")
            else:
                if (re.search(pattern_s, result[0])):
                    if not result[1].strip('\"').isalnum():
                        pass
                        
                elif(re.search(pattern_i, result[0])):
                    if not result[1].isdigit():
                        error_count += 1
                        self.log_path.write_text(self.log_path.read_text()+'Value in line ' + str(string_num) + ' should be an integer number\n')
                elif(re.search(pattern_f,result[0])):
                    try:
                        float(result[1])
                    except ValueError:
                        error_count += 1
                        self.log_path.write_text(self.log_path.read_text()+'Value in line' + str(string_num) + ' should be a floating pt value\n')
                else:
                    self.log_path.write_text (self.log_path.read_text()+"Error - unidentified parameter in line "+string_num+'\n')
                    error_count += 1
            string_num += 1
        return error_count
    
    def analyze_print(self,strings):
        '''Analyze report yaml'''
        error_count=0
        pattern_s=r'type|param|data|content'
        for string in strings:
            if (string.strip(' ') == '---' or string.strip(' ') == '-' or string.strip(' ') == 'content:'):
                string_num += 1
                continue
            result=string.strip(' ').rsplit(': ') 
            if (len(result) != 2):
                error_count += 1
                self.log_path.write_text(self.log_path.read_text()+"Error in line " + str(string_num)+ " - every string in yaml file should be a <parameter>: <value>\n")
            else:
                if not re.search(pattern_s, result[0]):
                    error_count += 1
                    self.log_path.write_text (self.log_path.read_text()+"Error - unidentified parameter in line "+string_num+'\n')
            num_string +=1 
        return error_count
