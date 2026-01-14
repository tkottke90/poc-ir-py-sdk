import argparse
import irsdk

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='iRacing telemetry parser and monitor')
  parser.add_argument('--file', help='Path to iRacing telemetry file (e.g., replay.ibt)')
  
  args = parser.parse_args()

  ir = irsdk.IRSDK()
  ir.open(args.file)

  weekend = ir['WeekendInfo']

  print(ir.var_headers_names)

