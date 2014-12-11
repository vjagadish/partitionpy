import matplotlib.pyplot as plt

system = 'kafka'

for line in open(system + '.out', 'r'):
  line = line.split(':')
  line[2] = line[2][:-1]
  if line[1] == 'True':
    plt.plot(int(line[0]), line[2], 'go')
  else:
    plt.plot(int(line[0]), line[2], 'ro')

plt.ylim([0, 1.4])
plt.xlabel('Iteration')
plt.ylabel('Latency')

#plt.show()
plt.savefig(system)
