import seaborn as sns
import pandas as pd
from matplotlib.pylab import plt
under_cutoff = lambda n: df[df[n] < 4][n].tail(45)

df = pd.read_csv('pyuv_vs_sync_times.csv', names=['seq', 'pyuv'])
sns.kdeplot(under_cutoff('seq'), bw=.05)
sns.kdeplot(under_cutoff('pyuv'), bw=.05)
plt.show()
