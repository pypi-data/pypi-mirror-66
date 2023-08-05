# theme_eliiza
Ggplot theme for eliiza

Sample usage

```python
from plotnine import * 
from plotnine.data import *
from eliiza_plotnine import theme_eliiza, eliiza_navy
(ggplot(mpg) + 
    geom_bar(aes(x='class'), fill = eliiza_navy) + 
    theme_eliiza() + 
    ggtitle("Number of cars sampled per Car Type"))
```
