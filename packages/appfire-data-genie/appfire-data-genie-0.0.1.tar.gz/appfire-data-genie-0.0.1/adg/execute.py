import click
import sys
import questionary
import logging
import jaydebeapi as jdbc
import jpype
import os
import string
import random
from random import randint

jar = './h2-1.4.200.jar'
os.environ['JAVA_HOME'] = '/Library/Java/JavaVirtualMachines/jdk1.8.0_202.jdk/Contents/Home/bin'
os.environ['CLASSPATH'] = jar

args = '-Djava.class.path=%s' % jar
jvm_path = jpype.getDefaultJVMPath()
jpype.startJVM(jvm_path, args)

# conn = jdbc.connect("org.h2.Driver",  # driver class
#                         "jdbc:h2:tcp://localhost:9092//Users/Lava/work/wittified/p2/p2-new/announcer/target"
#                         "/confluence/home/database/h2db",
#                         # JDBC url
#                         ["sa", ""],  # credentials
#                         "./h2-1.4.200.jar")  # location of H2 jar

@click.command()
@click.option('--verbose', '-v', is_flag=True, help="Verbose output")
@click.option('--database-url', '-dburl', help="Database URL string")
@click.option('--username', '-u', help="DB username")
@click.option('--password', '-p', help="DB password")
@click.argument('command')
def process(verbose, database_url, username, password, command):
    """
    Generates random data at the given database and application
    """

    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, stream=sys.stdout, format="%(message)s")
    logger = logging.getLogger("adg")
    
    conn = jdbc.connect("org.h2.Driver",  # driver class
                        database_url,
                        # JDBC url
                        [username, password],  # credentials
                        "./h2-1.4.200.jar")  # location of H2 jar
    logger.info(f'Database_URL: {database_url}')
    if command == 'run':
        count = questionary.text("Number of notifications? ").ask()
        type = questionary.select(
            "Type of Notifications?",
            choices=[
                'random',
                'banner',
                'flag',
                'fullpage',
                'dialog'
            ]).ask()  # returns value of selection
        type = 'intercept' if type == 'fullpage' else type
        try:
            curs = conn.cursor()
            if type == 'random':
                for x in range(0, int(count)):
                    curs.execute(
                        "INSERT INTO \"AO_13A15E_NOTIFICATION\" VALUES (true,false,'Dismiss',false,false," + "'" + ''.join(random.choice(string.ascii_lowercase) for x in range(1, 10)) +"',0,parsedatetime('17-09-2012 18:47:52.69', 'dd-MM-yyyy hh:mm:ss.SS'),false,false,false,0,null," + "'" + ''.join(random.choice(string.ascii_lowercase) for x in range(1, 10)) +"'," + str(
                            randint(10000, 1000000)) + ",false,0,false,true,parsedatetime('17-09-2012 18:47:52.69', 'dd-MM-yyyy hh:mm:ss.SS'),'::', ' ',true," + "'" + ''.join(
                            random.choice(string.ascii_uppercase) for x in range(1, 6)) +"'" + " ,null, " + "'" + random.choice(['banner', 'flag', 'intercept', 'dialog']) + "')")
            else:
                for x in range(0, int(count)):
                    curs.execute(
                        "INSERT INTO \"AO_13A15E_NOTIFICATION\" VALUES (true,false,'Dismiss',false,false,"'" + ''.join(random.choice(string.ascii_lowercase) for x in range(1, 10)) +"'",0,parsedatetime('17-09-2012 18:47:52.69', 'dd-MM-yyyy hh:mm:ss.SS'),false,false,false,0,null," + "'" + ''.join(random.choice(string.ascii_lowercase) for x in range(1, 10)) +"'," + str(
                            randint(10000, 1000000)) + ",false,0,false,true,parsedatetime('17-09-2012 18:47:52.69', 'dd-MM-yyyy hh:mm:ss.SS'),'::', ' ',true," + "'" + ''.join(
                            random.choice(string.ascii_uppercase) for x in range(1, 6)) +"'" + " ,null, " + "'" + type + "')")
    
        finally:
            if curs is not None:
                curs.close()
            if conn is not None:
                conn.close()


if __name__ == "__main__":
    process()
