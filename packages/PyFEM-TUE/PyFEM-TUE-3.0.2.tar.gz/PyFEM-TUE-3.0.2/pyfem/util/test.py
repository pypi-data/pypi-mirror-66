class nodeTable : pass

def readNodeTable( fileName , label ):

  fin = open( fileName , 'r' )

  startLabel = str('<'+label)
  endLabel   = str('</'+label)

  output = []

  for line in fin:
 
    if line.startswith(startLabel) == True:

      nt = nodeTable()

      nt.label    = label
      nt.subLabel = "None"
      nt.data     = []

      if 'name' in line:
        subLabel = line.split('=')[1].replace('\n','').replace('>','').replace(' ','').replace('\"','').replace('\'','')
        nt.subLabel = subLabel

        for line in fin:

          if line.startswith(endLabel) == True:
            output.append(nt)
            break
        
          a = line.strip().split(';')
      
          if len(a) == 2:
            b = a[0].split('=')
        
            if len(b) == 2:
              c = b[0].split('[')
              
              dofType = c[0]
              nodeID  = eval(c[1].split(']')[0])
             
              nt.data.append([ dofType,nodeID,eval(b[1]) ])
  
  return output
          
fn = "test.dat"

tt = readNodeTable( fn , "NodeConstraints")

print(len(tt))

print(tt[0].data[0][2])
for t in tt:
  print("aa",t.subLabel,len(t.data))
  for d in t.data:
    print("123",d[0],d[1],d[2])
