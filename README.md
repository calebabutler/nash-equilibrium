# nash-equilibrium
A simple simulation program of the iterated prisoner's dilemma

|                              | always defect      | always collaborate   | tit-for-tat        | random             | tit-for-tat with forgiveness   | tit-for-tat with reputation   | randomness with reputation   |
|------------------------------|--------------------|----------------------|--------------------|--------------------|--------------------------------|-------------------------------|------------------------------|
| always defect                | (2999.86, 2999.86) | (8999.59, 1999.91)   | (3005.86, 2998.86) | (6071.35, 2487.95) | (3658.09, 2890.16)             | (3005.86, 2998.86)            | (4889.73, 2684.89)           |
| always collaborate           |                    | (5999.73, 5999.73)   | (5999.73, 5999.73) | (3988.61, 7508.07) | (5999.73, 5999.73)             | (5999.73, 5999.73)            | (3240.11, 8069.44)           |
| tit-for-tat                  |                    |                      | (5999.73, 5999.73) | (4931.17, 4934.82) | (5999.73, 5999.73)             | (5999.73, 5999.73)            | (4323.59, 4328.49)           |
| random                       |                    |                      |                    | (4971.96, 5000.70) | (5268.64, 4904.19)             | (4997.09, 4993.61)            | (4044.64, 5390.23)           |
| tit-for-tat with forgiveness |                    |                      |                    |                    | (5999.73, 5999.73)             | (5999.73, 5999.73)            | (4219.56, 4692.98)           |
| tit-for-tat with reputation  |                    |                      |                    |                    |                                | (5999.73, 5999.73)            | (4720.04, 2719.00)           |
| randomness with reputation   |                    |                      |                    |                    |                                |                               | (4350.09, 4254.62)           |

![](https://github.com/calebabutler/nash-equilibrium/blob/main/plots.png)
