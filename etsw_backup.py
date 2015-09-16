#!/usr/bin/python
# @author Ivan Ceradini ivan.ceradini<at>ethicalsoftware.net
# G.P.L License
"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys, getopt
import subprocess

class EtswBackup:
    def __init__(self,tape,filename, logfile, verbose):
        self.tape= tape
        self.filename= filename
        self.verbose= verbose
        if( logfile != None ):
            self.logfile= open( logfile,"a" )
        else:
            self.logfile= sys.stdout
    def run_cmd(self, cmd ):
        if( self.verbose ):
            print(cmd)
        process= subprocess.Popen( cmd.split(), stdout=subprocess.PIPE)
        output= process.communicate()[0]
        print( output, self.logfile )
    def rewind(self):
        cmd= "mt -f %s rewind"%(self.tape)
        self.run_cmd(cmd)
    def tell(self):
        cmd= "mt -f %s tell"%(self.tape)
        self.run_cmd(cmd)
    def list( self ):
        cmd= "tar -tzf %s %s"%(self.tape, self.filename)
        self.run_cmd(cmd)
    def backup(self):
        cmd= "tar -czf %s %s"%(self.tape, self.filename)
        self.run_cmd(cmd)
    def compare(self):
        cmd= "tar -dlpMzvf %s %s"%(self.tape, self.filename)
        self.run_cmd(cmd)
    def restore(self):
        cmd= "tar -xlpMzvf %s %s"%(self.tape, self.filename)
        self.run_cmd(cmd)

def print_help():
    print( "-h  : this help " )
    print( "-c  --command <command> ( *backup, restore, list, compare, rewind ) *default ")
    print( "-d  --dir <directory_to_backup> (* current_dir ) ")
    print( "-f  --file <file_to_backup> ")
    print( "-o --output <outputfile> default stdout")
    print( "-t  --tape <drive_or_file_backup> (*/dev/st0) ")
    print( "-v  --verbose  ( * quite) ")
    
def main(argv):
    tape,logfile,command,filename,verbose= '/dev/st0',None,'backup','.',False
    try:
        opts,args = getopt.getopt(argv,"ht:o:c:f:d:",["tape=","logfile=","command=","file=","dir="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-t", "--tape"):
            tape= arg
        elif opt in ("-o", "--logfile"):
            logfile= arg
        elif opt in ("-c", "--command"):
            command= arg
        elif opt in ("-f", "--file", "-d", "--dir"):
            filename= arg
        elif opt in ("-v", "--verbose"):
            verbose= arg
    if( command== None ):
        print_help()
    bck= EtswBackup( tape,filename,logfile, verbose)
    cmd= "bck.%s()"%command
    eval(cmd) 
    print( cmd )
    sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])
