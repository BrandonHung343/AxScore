import csv
import os
import errno
import stat
import sys
import getopt

''' System for entering data entries on the command line. To use, run file 
    from command line. Comes with one argument:
        -n, to delete old data file and make a new one
    Otherwise, it simply appends on the old data file (or automatically 
    creates one if one is not present. Prompt will walk you through how
    to use in a user-friendly manner '''

def main():
    unixOptions = "n"
    gnuOptions = ["new"]
    argpassed = sys.argv[1:]
    filename = ('axdata.csv')
    fieldnames = ['Points', 'Name of Image File', 'General Comments']
    pathName = os.getcwd() + '/' + filename

    try:
        if argpassed is not None and len(argpassed) > 0:
            arguments, values = getopt.getopt(argpassed, unixOptions, gnuOptions)
            print(arguments)
            if arguments[0][0] in ('-n', '--new'):
                print("New option detected. Deleting old file...")
                if os.path.exists(pathName):
                    os.remove(filename)
                    print('File deleted')

    except Exception as e:
        print("Something went wrong: exception occured (%s)" % (e))
       
    print('Welcome! Setting up...')
    if not os.path.exists(os.path.dirname(filename)) :
        try:
            f = open(filename, 'w+')
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            f.close()
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise Exception('File does not exist, and there was a problem creating it')

    while True:
        with open(filename, mode='a') as fi:
            writer = csv.DictWriter(fi, fieldnames=fieldnames)
            print('Begin writing to file. Type in "quit" or "exit" at any time to exit"')
            points = input('Please list the throw\'s point value:\n')
            if points == 'quit' or points == 'exit':
                break
            img_name = input('Please list the name of the image file containing this throw:\n')
            if img_name == 'quit' or img_name == 'exit':
                break
            gen_comments = input('Please list any general comments about what happened during throw:\n')
            if gen_comments == 'quit' or gen_comments == 'exit':
                break
            values = [points, img_name, gen_comments]
            print('Point value = %s, Name of image = %s, Comments = %s ' % (points, img_name, gen_comments))
            correct = input('Is the above information correct? y/n to continue\n')
            if correct != 'y':
                print('Discarding data')
                continue
            writer.writerow(dict(zip(fieldnames, values)))
            print('Entering data now')
    print('Closing file now. Goodbye!')

if __name__ == '__main__':
    main()




        
        

       
