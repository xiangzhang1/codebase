# POSCAR

    pad=10A

Bourbaki 文献指出 15-20 Å，Bourbaki 测试指出 10 Å。取 10 Å 以求快。

# INCAR

    # mode
    ISTART = 0
    ICHARG = 2
    
    ISIF=2
    IBRION = 2
    NSW = 1000
    
显然。**问题是**，我们此前的所有计算都取 `ISIF=0`，所幸理论上应该没有影响。

    EDIFF = 1E-5
    EDIFFG = -0.02
    
完全符合 Bourbaki 文献，和 Bourbaki 测试。

    ISYM = 0
    
既然我们在研究病态的优化，自然。

    # dft
    ENCUT = 400
    ISPIN = 2
    PREC = Normal
    
完全符合 Bourbaki 文献，和 Bourbaki 测试。

    ISMEAR = 0
    SIGMA = 0.01
    
没有 Bourbaki 文献，没有 Bourbaki 测试。
**问题是**，不完全符合 VASP wiki：金属 0/0.1，非金属/未知 0/0.03-0.05。
符合 Yun 的 INCAR。

    LREAL = Auto
    
没有 Bourbaki 文献。
**问题是**，勉强符合 Bourbaki 测试：On/Off 无影响，之前的所有计算都取 On。
符合 VASP wiki。

    # behavior
    LWAVE = .FALSE.
    LORBIT = 11

没有影响。

# KPOINTS

# POTCAR

`Pb_d`  符合 VASP manual。Bourbaki 测试无记载，但记忆中无区别。
