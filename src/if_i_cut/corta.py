'''
Created on 12/09/2016

@author: ernesto
'''


import logging
import sys
import fileinput

logger_cagada = None
nivel_log = logging.ERROR
#nivel_log = logging.DEBUG

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

                assert(abs(intersex_y - intersex_y_tmp) < 0.000000001)

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
                self.lineas_sin_filtrar = []
                self.putos_intersex = []

        def anade_linea(self, linea):
                borro_al_menos_1_linea = False
                
                num_lineas_orig = len(self.lineas)
                
                self.lineas_sin_filtrar.append(linea)
                self.lineas.append(linea)
                if(num_lineas_orig == 0):
                        return


                if(num_lineas_orig == 1):
                        assert(not len(self.putos_intersex))

                        nueva_intersex = Punto.genera_intersex(linea, self.lineas[-2])
                        logger_cagada.debug("nueva intersez entre %s y %s es %s" % (linea, self.lineas[-2], nueva_intersex))
                        self.putos_intersex.append(nueva_intersex)

                        return

                nueva_intersex = Punto.genera_intersex(linea, self.lineas[-3])
                logger_cagada.debug("nueva intersez entre %s y %s es %s" % (linea, self.lineas[-3], nueva_intersex))
                logger_cagada.debug("los putos intersex %s" % self.putos_intersex)
                while (len(self.putos_intersex) >= 1):
                        logger_cagada.debug("comparando intersex nueva %s con %s" % (nueva_intersex, self.putos_intersex[-1]))
                        if(Punto.esta_a_abajo_b(nueva_intersex, self.putos_intersex[-1])):
                                logger_cagada.debug("borrando %s %s" % (self.putos_intersex[-1], self.lineas[-2]))
                                del self.putos_intersex[-1]
                                del self.lineas[-2]
                                borro_al_menos_1_linea = True
                        else:
                            break

                if(not borro_al_menos_1_linea):
                    nueva_intersex = Punto.genera_intersex(linea, self.lineas[-2])
                    logger_cagada.debug("se sustituyo el intersex por %s" % nueva_intersex)
                self.putos_intersex.append(nueva_intersex)

        def puto_en_linea_minima(self, x):
                idx_linea_min = -1
                idx_puto_intersex = -1
                puto_minimo = None
                
                puto_minimo = Punto(sys.maxsize, sys.maxsize)

                for idx_intersex in range(self.ultimo_idx_min, len(self.putos_intersex)):
                    puto_intersex = self.putos_intersex[idx_intersex]
                    if(x < puto_intersex.x):
                        idx_puto_intersex = idx_intersex
                        break
                
                idx_linea_min = idx_puto_intersex
                puto_minimo = self.lineas[idx_linea_min].evalua_puto(x)
                    
                self.ultimo_idx_min = idx_puto_intersex
                
                logger_cagada.debug("el puto de intersex para x %u es %s" % (x, self.putos_intersex[idx_puto_intersex]))
                
                logger_cagada.debug("el puto min de %u se alcanza con linea %s, es %s" % (x, self.lineas[idx_linea_min], puto_minimo))
                
                return puto_minimo
            
        def puto_en_linea_minima_lentote(self, x):
                puto_minimo = None
                linea_min = None
                
                puto_minimo = Punto(sys.maxsize, sys.maxsize)
                
#                logger_cagada.debug("las lineas sin filtrar %s" % self.lineas_sin_filtrar)

                for linea in self.lineas_sin_filtrar:
                    puto_actual = None
                    
                    puto_actual = linea.evalua_puto(x)
                    
                    if(puto_actual.y < puto_minimo.y):
                        puto_minimo = puto_actual
                        linea_min = linea
                        
                logger_cagada.debug("el puto min de %u se alcanza con linea %s, es %s" % (x, linea_min, puto_minimo))
                
                return puto_minimo
            
        def resetear_estado(self):
            self.ultimo_idx_min = 0
                    
                
def corta_rosa_generar_lineas(lineas, valores_a, valores_b, lineas_de_a, valores_pos_x):
    tam_a = 0
    tam_b = 0
    tam_mayor = 0
    suma_actual = 0
    valores_mayor = []
    
    tam_a = len(valores_a)
    tam_b = len(valores_b)
    
    if(tam_a > tam_b):
        valores_mayor = sorted(valores_a)
        valores_pos_x += sorted(valores_b)
        lineas_de_a = True
    else:
        valores_mayor = sorted(valores_b)
        valores_pos_x += sorted(valores_a)
        lineas_de_a = False
    
    tam_mayor = len(valores_mayor)
    
    logger_cagada.debug("los valores q aran lineas %s" % valores_mayor)
    lineas.append(Linea(tam_mayor + 1, 0))
    for idx_valor, valor in enumerate(valores_mayor):
        suma_actual += valor
        nueva_linea = Linea(tam_mayor - idx_valor , suma_actual)
        lineas.append(nueva_linea)
    
    logger_cagada.debug("las lineas degeneradas %s" % lineas)
    
def corta_rosa_core(numeros_a, numeros_b):
    son_lineas_de_a = False
    that_u_are = 0
    lineas = []
    valores_x = []
    convexo_caca = None
    
    corta_rosa_generar_lineas(lineas, numeros_a, numeros_b, son_lineas_de_a, valores_x)
    
    convexo_caca = ConvexoHull()
    
    for linea in lineas:
        convexo_caca.anade_linea(linea)
        
    logger_cagada.debug("las lienas sobreviv %s" % convexo_caca.lineas)
    logger_cagada.debug("why wont %s" % valores_x)
    for pos_x in valores_x:
        puto_min = None
        puto_min_validacion = None
        
        puto_min = convexo_caca.puto_en_linea_minima(pos_x)
        if(nivel_log == logging.DEBUG):
            puto_min_validacion = convexo_caca.puto_en_linea_minima_lentote(pos_x)
        
            logger_cagada.debug("anyway %s, %s" % (puto_min, puto_min_validacion))
        
            assert abs(puto_min.y - puto_min_validacion.y) < 0.000000001, "en punto x %u el puto min %f, el min de valida %f" % (pos_x, puto_min.y, puto_min_validacion.y) 
        
        that_u_are += puto_min.y
    
    logger_cagada.debug("la suma total %lu" % that_u_are)
    
    that_u_are += lineas[-1].desplazamiento
    logger_cagada.debug("la suma con valor inicial %lu" % that_u_are)
    
    return that_u_are
        
def corta_rosa_main():
    num_casos = 0
    lineas = []
    
    lineas = list(fileinput.input())
    
    num_casos = int(lineas[0].strip())
    
    logger_cagada.debug("los momentos %u" % num_casos)
    
    for idx_caso in range(num_casos):
        num_as = 0
        num_bs = 0
        chosto_min = 0
        valores_a = []
        valores_b = []
        linea = ""
        
        logger_cagada.debug("when u scream %s" % lineas[idx_caso * 3 + 1].strip())
        num_as, num_bs = (int(mierda) for mierda in lineas[idx_caso * 3 + 1].strip().split())
        
        valores_a = [int(mierda) for mierda in lineas[idx_caso * 3 + 2].strip().split()]
        valores_b = [int(mierda) for mierda in lineas[idx_caso * 3 + 3].strip().split()]
        
        logger_cagada.debug("valores a %s, valores b %s" % (valores_a, valores_b))
        
        assert num_as - 1 == len(valores_a), "el num establecido de valores a %u, el q c encontro %u" % (num_as, len(valores_a))
        assert num_bs - 1 == len(valores_b), "el num establecido de valores a %u, el q c encontro %u" % (num_bs, len(valores_b))
        
        chosto_min = corta_rosa_core(valores_a, valores_b)
        
        print("%u" % (chosto_min % (int(1E9) + 7)))
        
        
        

if __name__ == '__main__':
        FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(level=nivel_log, format=FORMAT)
        logger_cagada = logging.getLogger("asa")
        logger_cagada.setLevel(nivel_log)


        corta_rosa_main()
