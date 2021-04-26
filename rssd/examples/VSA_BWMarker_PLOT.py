import pandas as pd
import matplotlib.pyplot as plt

f = __file__.split('_PLOT')[0] + '.txt'
f = 'VSA_BWMarker.py-210426.csv'
print(f)
df = pd.read_csv(f, header=0, skiprows=1, sep=',')
print(f'Cols: {list(df.columns)}')                  # Col names

# ## Define Pivot Table
Yval = ['MkrBndPwr']                                # Y Values
Xval = ['RBW']                                      # X Values
Cols = ['SwpTime']                                  # Separate Lines
aggg = 'mean'                                       # mean | sum
table = pd.pivot_table(df, values=Yval, index=Xval, columns=Cols, aggfunc=aggg)
print(f'Traces:{table.shape[1]} DataPts:{table.shape[0]}')

# ##############################################################################
# ## Plot Data
# ##############################################################################
table.plot(legend=True)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3)
plt.tight_layout(pad=2)
plt.grid()
plt.title(f'{Yval} {aggg}')
# plt.axis([-50, 10, -60, -20])                     # X, Y
plt.ylim((-88, -82))
plt.xlabel(Xval)
plt.ylabel(Yval)

plt.savefig(f'{f}.png')
plt.show(block=False)
plt.pause(3)
plt.close()
