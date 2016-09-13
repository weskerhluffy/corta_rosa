'''
Created on 12/09/2016

@author: ernesto
'''


import logging
import sys

logger_cagada = None
# nivel_log = logging.ERROR
nivel_log = logging.DEBUG

class Linea():
        def __init__(self, pendiente, desplazamiento):
                self.pendiente = pendiente
                self.desplazamiento = desplazamiento

        def __str__(self):
                return "Linea y = %dx + %d" % (self.pendiente, self.desplazamiento)

        def evalua_puto(self, x):
                y = 0

                y = self.pendiente * x + self.desplazamiento

                return Punto(x, y)
            
        def __repr__(self):
            return self.__str__()

class Punto():
        def __init__(self, x, y):
                self.x = x
                self.y = y

        @staticmethod
        def genera_intersex(linea_a, linea_b):
                pend_a = 0
                pend_b = 0
                desp_a = 0
                desp_b = 0
                intersex_x = 0.0
                intersex_y = 0.0
                intersex_y_tmp = 0.0

                logger_cagada.debug("if i cut off a %s b %s" % (linea_a, linea_b))
                
                pend_a = linea_a.pendiente
                desp_a = linea_a.desplazamiento
                pend_b = linea_b.pendiente
                desp_b = linea_b.desplazamiento
                intersex_x = float(desp_b - desp_a) / float(pend_a - pend_b) 
                
                logger_cagada.debug("la intersex x %f" % intersex_x)
                
                intersex_y = float(pend_b * desp_a - pend_a * desp_b) / float(pend_b - pend_a)

                intersex_y_tmp = float(pend_a * intersex_x + desp_a)
                
                logger_cagada.debug("love me anyway %f y tmp %f" % (intersex_y, intersex_y_tmp))

                assert(intersex_y - intersex_y_tmp < 0.000000001)

                return Punto(intersex_x, intersex_y)

        def __str__(self):
                return "Puto x:%f y:%f" % (self.x, self.y)

        @staticmethod
        def esta_a_abajo_b(puto_a, puto_b):
                abajo = False
                x_a = 0
                x_b = 0
                y_a = 0
                y_b = 0

                x_a = puto_a.x
                y_a = puto_a.y

                x_b = puto_b.x
                y_b = puto_b.y

                abajo = y_a < y_b
                assert(not abajo or x_a <= x_b)

                return abajo
            
        def __repr__(self):
            return self.__str__()
                

class ConvexoHull():
        def __init__(self):
                self.ultimo_idx_min = 0
                self.lineas = []
                self.putos_intersex = []

        def anade_linea(self, linea):
                num_lineas_orig = len(self.lineas)
                
                if(num_lineas_orig == 0):
                        self.lineas.append(linea)
                        return

                self.lineas.append(linea)
                nueva_intersex = Punto.genera_intersex(linea, self.lineas[-2])
                logger_cagada.debug("nueva intersez entre %s y %s es %s" % (linea, self.lineas[-2], nueva_intersex))

                if(num_lineas_orig == 1):
                        assert(not len(self.putos_intersex))

                        self.putos_intersex.append(nueva_intersex)

                        return

                logger_cagada.debug("los putos intersex %s" % self.putos_intersex)
                while (len(self.putos_intersex) >= 1):
                        logger_cagada.debug("comparando intersex nueva %s con %s" % (nueva_intersex, self.putos_intersex[-1]))
                        if(Punto.esta_a_abajo_b(nueva_intersex, self.putos_intersex[-1])):
                                logger_cagada.debug("borrando %s %s" % (self.putos_intersex[-1], self.lineas[-2]))
                                del self.putos_intersex[-1]
                                del self.lineas[-2]
                        else:
                            break

                self.putos_intersex.append(nueva_intersex)

        def puto_en_linea_minima(self, x):
                idx_linea_min = -1
                puto_minimo = None
                
                if(self.ultimo_idx_min < (len(self.lineas) - 1)):
                    puto_minimo = Punto(sys.maxsize, sys.maxsize)
    
                    for idx_linea in range(self.ultimo_idx_min, len(self.lineas)):
                        puto_actual = None
                        
                        puto_actual = self.lineas[idx_linea].evalua_puto(x)
                        
                        if(puto_actual.y < puto_minimo.y):
                            puto_minimo = puto_actual
                            idx_linea_min = idx_linea
                            
                    assert(idx_linea_min > -1)
                    
                    self.ultimo_idx_min = idx_linea_min
                else:
                    puto_minimo = self.lineas[-1].evalua_puto(x)
                    
                return puto_minimo
                    
                
def generar_lineas(lineas, valores_a, valores_b):
    tam_a = 0
    tam_b = 0
    valores_mayor = ()
    valores_menor = ()
    
    tam_a = len(valores_a)
    tam_b = len(valores_b)
    
    if(tam_a > tam_b):
        valores_mayor = sorted(valores_a, reverse=True)
        valores_menor = sorted(valores_b)
    else:
        valores_mayor = sorted(valores_b, reverse=True)
        valores_menor = sorted(valores_a)
                        
                    
                                

if __name__ == '__main__':
        lineas = []
        
        convex = None
    
        FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(level=nivel_log, format=FORMAT)
        logger_cagada = logging.getLogger("asa")
        logger_cagada.setLevel(nivel_log)


        lineas = [Linea(1020, 234), Linea(844, 2344), Linea(222, 332), Linea(221, 343)]
        
        convex = ConvexoHull()
        
        for linea in lineas:
            convex.anade_linea(linea)
            
        logger_cagada.debug("would ya still lineas %s intersex %s" % (convex.lineas, convex.putos_intersex))
