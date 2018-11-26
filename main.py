from error_parser import parser as ep

parser1 = ep.LogParser('logs')
parser1.print_errors()


parser2 = ep.LogParser('logs\\2018.03.02')
parser2.print_errors()

parser3 = ep.LogParser('logs', 'log.txt')
parser3.print_errors()

