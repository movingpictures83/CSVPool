def removeDup(x):
   y = []
   for i in range(len(x)):
      if (x[i] not in y):
         y.append(x[i])
   return y

class CSVPoolPlugin:
   def input(self, inputfile):
      self.inputfile = inputfile
      filestuff = open(self.inputfile, 'r')
      self.counts = dict()
      # Read once, just to get row and column headers
      firstline = filestuff.readline().strip()
      self.colnames = firstline.split(',')
      if self.colnames.count('\"\"') != 0:
         self.colnames.remove('\"\"')
      for i in range(len(self.colnames)):
         column = self.colnames[i]
         # Remove trailing digits up to and including underscore
         if (column.find('UCG') == -1):
            stoppos = len(column)-1
            quoteflag = False
            if (column[stoppos] == '\"'):
               stoppos -= 1
               quoteflag = True
            if (column[stoppos].isdigit()):
               while (stoppos != 0 and column[stoppos].isdigit()):
                  stoppos -= 1
            if (stoppos != 0 and column[stoppos] == '_'):
               column = column[:stoppos]
               if (quoteflag):
                  column += '\"'
            self.colnames[i] = column

      self.rownames = []
      for line in filestuff:
         contents = line.split(',')
         self.rownames.append(contents[0])

      for row in self.rownames:
         if (row not in self.counts):
            self.counts[row] = dict()
         for col in self.colnames:
            self.counts[row][col] = 0

      filestuff.close()

   def run(self):
      # Now open again, to get counts
      filestuff = open(self.inputfile, 'r')
      disregard = filestuff.readline()

      for line in filestuff:
         contents = line.split(',')
         row = contents[0]
         for i in range(1,len(contents)):
            self.counts[row][self.colnames[i-1]] += int(contents[i])

        

   def output(self, outputfile):
       # Remove duplicates
       self.rownames = removeDup(self.rownames)
       self.colnames = removeDup(self.colnames)

       filestuff = open(outputfile, 'w')
       filestuff.write('\"\",')
       for j in range(len(self.colnames)):
          filestuff.write(self.colnames[j])
          if (j != len(self.colnames)-1):
             filestuff.write(',')
          else:
             filestuff.write('\n')

       for i in range(len(self.rownames)):
          filestuff.write(self.rownames[i]+",")
          for j in range(len(self.colnames)):
             filestuff.write(str(self.counts[self.rownames[i]][self.colnames[j]]))
             if (j != len(self.colnames)-1):
                filestuff.write(',')
             else:
                filestuff.write('\n')
          
             
