
#!/usr/bin/env python3
__author__ = "Azat Artificial Intelligence, LLP (AzatAI)"
__copyright__ = "Copyright 2020, AzatAI"
__credits__ = ["Yaakov Azat", ]
__license__ = "MIT"
__version__ = "0.0.0"
__maintainer__ = "Yaakov Azat"
__email__ = "yaakovazat@gmail.com"
__status__ = "Development"

"""

                                                                                                                                    
                                                                                                                                    
               AAA                                                          tttt                        AAA               IIIIIIIIII
              A:::A                                                      ttt:::t                       A:::A              I::::::::I
             A:::::A                                                     t:::::t                      A:::::A             I::::::::I
            A:::::::A                                                    t:::::t                     A:::::::A            II::::::II
           A:::::::::A           zzzzzzzzzzzzzzzzz  aaaaaaaaaaaaa  ttttttt:::::ttttttt              A:::::::::A             I::::I  
          A:::::A:::::A          z:::::::::::::::z  a::::::::::::a t:::::::::::::::::t             A:::::A:::::A            I::::I  
         A:::::A A:::::A         z::::::::::::::z   aaaaaaaaa:::::at:::::::::::::::::t            A:::::A A:::::A           I::::I  
        A:::::A   A:::::A        zzzzzzzz::::::z             a::::atttttt:::::::tttttt           A:::::A   A:::::A          I::::I  
       A:::::A     A:::::A             z::::::z       aaaaaaa:::::a      t:::::t                A:::::A     A:::::A         I::::I  
      A:::::AAAAAAAAA:::::A           z::::::z      aa::::::::::::a      t:::::t               A:::::AAAAAAAAA:::::A        I::::I  
     A:::::::::::::::::::::A         z::::::z      a::::aaaa::::::a      t:::::t              A:::::::::::::::::::::A       I::::I  
    A:::::AAAAAAAAAAAAA:::::A       z::::::z      a::::a    a:::::a      t:::::t    tttttt   A:::::AAAAAAAAAAAAA:::::A      I::::I  
   A:::::A             A:::::A     z::::::zzzzzzzza::::a    a:::::a      t::::::tttt:::::t  A:::::A             A:::::A   II::::::II
  A:::::A               A:::::A   z::::::::::::::za:::::aaaa::::::a      tt::::::::::::::t A:::::A               A:::::A  I::::::::I
 A:::::A                 A:::::A z:::::::::::::::z a::::::::::aa:::a       tt:::::::::::ttA:::::A                 A:::::A I::::::::I
AAAAAAA                   AAAAAAAzzzzzzzzzzzzzzzzz  aaaaaaaaaa  aaaa         ttttttttttt AAAAAAA                   AAAAAAAIIIIIIIIII
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                    
                                                                                                                                                                                                          
"""
from setuptools import setup

setup(
    name='gitset',
    version='0.1',
    py_modules=['gitset'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        gitset=gitset:cli
    ''',
)