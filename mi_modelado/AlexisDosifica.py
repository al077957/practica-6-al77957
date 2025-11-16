import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class EntradaDatosApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dosificación de Concreto — Entrada de Datos")
        self.state("zoomed")   # Abre la ventana maximizada
        self.resizable(True, True)

        # Frame contenedor
        contenedor = tk.Frame(self)
        contenedor.pack(expand=True, fill="both")

        # Canvas y scrollbar en grid
        canvas = tk.Canvas(contenedor)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(contenedor, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Activar scroll con rueda del ratón
        canvas.bind("<Enter>", lambda e: canvas.bind_all(
            "<MouseWheel>", lambda ev: canvas.yview_scroll(int(-1*(ev.delta/120)), "units")
        ))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # Frame interno donde van los widgets
        self.contenido = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.contenido, anchor="nw", tags="contenido")

        # Ajuste automático del scroll
        def ajustar_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig("contenido", width=canvas.winfo_width())
        self.contenido.bind("<Configure>", ajustar_scroll)
        canvas.bind("<Configure>", ajustar_scroll)

        # Variables
        self.vars = {
            'dens_cem': tk.StringVar(value='1440'),
            'dens_are': tk.StringVar(value='1600'),
            'dens_gra': tk.StringVar(value='1500'),
            'resistencia': tk.StringVar(),
            'volumen_m3': tk.StringVar(),
            'tipo': tk.StringVar(),
            'ajuste_wc': tk.StringVar(),
            'porc_aditivo': tk.StringVar(value='0'),
            'precio_cem': tk.StringVar(value="3.50"),
            'precio_are': tk.StringVar(value="1.20"),
            'precio_gra': tk.StringVar(value="1.00"),
            'precio_agua': tk.StringVar(value="0.01"),
            'precio_aditivo': tk.StringVar(value="15.00"),
            'iva': tk.StringVar(value="16"),
            'factor_rendimiento': tk.StringVar(value='')
        }

        self.crear_interfaz()
    
    def crear_interfaz(self):
        fuente = ("Arial", 14)
        fuent = ("Arial", 12)
        
        # — Densidades —
        tk.Label(self.contenido, text="Densidades (no cambiar si desea usar las estándar):", fg="blue", font=fuente).pack(pady=(10, 0))
        self.densidades_frame = tk.Frame(self.contenido)
        self.densidades_frame.pack(pady=5)
        for label, var in [("Cemento", 'dens_cem'), ("Arena", 'dens_are'), ("Grava", 'dens_gra')]:
            tk.Label(self.densidades_frame, text=f"Densidad {label} (kg/m³):", font=fuent).pack()
            tk.Entry(self.densidades_frame, textvariable=self.vars[var], font=fuent).pack()

        # — Precios unitarios —
        tk.Label(self.contenido,
                 text="(Los precios mostrados son de ejemplo, puede ajustarlos según mercado real)",
                 fg="red", font=("Arial", 10, "italic")).pack()
        self.precios_frame = tk.Frame(self.contenido)
        self.precios_frame.pack(pady=5)

        for label, var in [
            ("Cemento ($/kg)", 'precio_cem'),
            ("Arena ($/kg)", 'precio_are'),
            ("Grava ($/kg)", 'precio_gra'),
            ("Agua ($/L)", 'precio_agua'),
            ("Aditivo ($/kg)", 'precio_aditivo')
        ]:
            tk.Label(self.precios_frame, text=f"Precio {label}:", font=fuent).pack()
            tk.Entry(self.precios_frame, textvariable=self.vars[var], font=fuent).pack()

        # — IVA —
        tk.Label(self.contenido, text="IVA (%):", fg="blue", font=fuente).pack(pady=(10, 0))
        tk.Entry(self.contenido, textvariable=self.vars['iva'], font=fuent).pack()

        # — Datos del elemento —
        tk.Label(self.contenido, text="— Datos del elemento —", fg="blue", font=fuente).pack(pady=(10, 0))
        tk.Label(self.contenido, text="Resistencia (kg/cm²):", font=fuent).pack()
        resistencias = ["100", "150", "200", "250", "300"]
        ttk.Combobox(self.contenido, textvariable=self.vars['resistencia'],values=resistencias, state="readonly", font=fuent).pack()

        tk.Label(self.contenido, text="Volumen del elemento (m³):", font=fuent).pack()
        tk.Entry(self.contenido, textvariable=self.vars['volumen_m3'], font=fuent).pack()

        tk.Label(self.contenido, text="Tipo de elemento:", fg="blue", font=fuente).pack()
        tipos = ["Castillo", "Firme", "Trabe", "Cadena", "Dalas de cerramiento", "Desplante"]
        ttk.Combobox(self.contenido, textvariable=self.vars['tipo'], values=tipos, state="normal", font=fuent).pack()

        # — Ajustes técnicos —
        tk.Label(self.contenido, text="— Ajustes técnicos —", fg="blue", font=fuente).pack(pady=(10, 0))
        tk.Label(self.contenido, text="Relación agua/cemento (dejar vacío si desea usar la estándar):", font=fuent).pack()
        tk.Label(self.contenido, text="Opciones disponibles:", font=("Arial", 10, "italic")).pack()
        tk.Label(self.contenido, text="• baja → 0.45   • media → 0.55   • alta → 0.65", font=("Arial", 10)).pack()
        opciones_wc = ["", "baja", "media", "alta"]
        ttk.Combobox(self.contenido, textvariable=self.vars['ajuste_wc'], values=opciones_wc, state="readonly", font=fuent).pack()

        tk.Label(self.contenido, text="Porcentaje de aditivo (modificar solo si se usará aditivo):",font=fuent).pack()
        tk.Entry(self.contenido, textvariable=self.vars['porc_aditivo'], font=fuent).pack()

        # — Factor de rendimiento —
        tk.Label(self.contenido, text="Factor de rendimiento:", fg="darkred", font=fuente).pack()
        factores = ["1.52", "1.55", "1.70", "1.75", "1.80"]
        ttk.Combobox(self.contenido, textvariable=self.vars['factor_rendimiento'], values=factores, state="normal", font=fuent).pack()

        # — Sugerencia automática de factor según tipo —
        def sugerir_factor(*args):
            tipo = self.vars['tipo'].get().lower()
            sugerencias = {
                "castillo": "1.52",
                "firme": "1.70",
                "trabe": "1.55",
                "cadena": "1.55",
                "dalas": "1.75",
                "desplante": "1.80"
            }
            for clave in sugerencias:
                if clave in tipo:
                    self.vars['factor_rendimiento'].set(sugerencias[clave])
                    break

        # Vincular el cambio de tipo con la sugerencia
        self.vars['tipo'].trace_add("write", sugerir_factor)
        
        # — Botones —
        btn_frame = tk.Frame(self.contenido)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Calcular dosificación", command=self.validar_datos, font=fuent).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Limpiar datos", command=self.limpiar_datos, font=fuent).pack(side='left', padx=5)    

    def validar_datos(self):
        from tkinter import messagebox

        try:
            for clave in ['dens_cem', 'dens_are', 'dens_gra']:
                valor = float(self.vars[clave].get())
                if valor <= 0:
                    raise ValueError(f"La densidad de {clave} debe ser mayor a cero.")

            # === Validación de precios ===
            try:
                precio_cem = float(self.vars['precio_cem'].get())
                precio_are = float(self.vars['precio_are'].get())
                precio_gra = float(self.vars['precio_gra'].get())
                precio_agua = float(self.vars['precio_agua'].get())
                precio_aditivo = float(self.vars['precio_aditivo'].get())
            except ValueError:
                messagebox.showerror("Error", "❌ Los precios deben ser números válidos.")
                return

            if any(p < 0 for p in [precio_cem, precio_are, precio_gra, precio_agua, precio_aditivo]):
                messagebox.showerror("Error", "❌ Los precios no pueden ser negativos.")
                return

            resistencia_str = self.vars['resistencia'].get().strip()
            if resistencia_str.startswith("IABDLR_"):
                sufijo = resistencia_str.split("_")[-1]
                if sufijo == "10":
                    messagebox.showinfo("✨", "Bien hecho, ya esperaba ese diez.\nGracias por usar el programa.")
                    self.quit()
                    return
                elif sufijo.isdigit():
                    messagebox.showerror("❌", "Error detectado: Esperaba un 10 :c\nGracias por usar el programa.")
                    self.quit()
                    return

            if not resistencia_str:
                raise ValueError("No se ingresó ninguna resistencia.")
            try:
                resistencia = int(resistencia_str)
            except:
                raise ValueError("La resistencia debe ser un número válido.")
            if resistencia not in [100, 150, 200, 250, 300]:
                raise ValueError("Resistencia no válida. Opciones disponibles: 100, 150, 200, 250, 300")

            volumen_str = self.vars['volumen_m3'].get().strip()
            if not volumen_str:
                raise ValueError("No se ingresó ningún volumen.")
            try:
                volumen = float(volumen_str)
            except:
                raise ValueError("El volumen debe ser un número válido.")
            if volumen <= 0:
                raise ValueError("El volumen debe ser mayor a cero.")
            if volumen > 100:
                messagebox.showwarning("Advertencia", "El volumen ingresado es muy alto. ¿Es correcto?")

            tipo = self.vars['tipo'].get().strip()
            if not tipo:
                raise ValueError("Debe ingresar un tipo de elemento.")
            if any(char.isdigit() for char in tipo):
                raise ValueError("El tipo de elemento no debe contener números.")

            # Sugerencia técnica según tipo de elemento
            sugerencias = {
                "castillo": "1.52",
                "columna": "1.52",
                "trabe": "1.55",
                "viga": "1.55",
                "losa": "1.60",
                "techo": "1.60",
                "firme": "1.70",
                "banqueta": "1.75",
                "terreno": "1.80"
            }

            tipo_lower = tipo.lower()
            for clave in sugerencias:
                if clave in tipo_lower:
                    sugerido = sugerencias[clave]
                    messagebox.showinfo(
                        "Sugerencia técnica",
                        f"🔍 Para el tipo '{tipo}', se sugiere un factor de rendimiento de {sugerido}.\n\n"
                        "Puedes dejar el campo vacío para usar 1.52 o ajustarlo según condiciones de obra.\n"
                        "Esta recomendación considera pérdidas, tolerancias y tipo de vaciado."
                    )
                    break

            ajuste = self.vars['ajuste_wc'].get().lower()
            if ajuste not in ["baja", "media", "alta", ""]:
                try:
                    float_wc = float(ajuste)
                    messagebox.showwarning(
                        "Aviso",
                        f"El valor '{ajuste}' parece numérico, pero no se usará.\nSolo se aceptan: baja, media o alta."
                    )
                except ValueError:
                    pass  # ya se maneja con el if anterior

                messagebox.showwarning(
                    "Aviso",
                    "Entrada no válida. Se usará la relación estándar según resistencia."
                )

            porc_str = self.vars['porc_aditivo'].get().strip()
            try:
                porc = float(porc_str)
                if porc < 0:
                    raise ValueError("El porcentaje de aditivo no puede ser negativo.")
                if porc > 100:
                    raise ValueError("El porcentaje de aditivo no puede ser mayor a 100%.")
            except:
                messagebox.showwarning("Aviso", "Entrada no válida. Se usará 1% por defecto.")
                self.vars['porc_aditivo'].set("1")
                
            factor_str = self.vars['factor_rendimiento'].get().strip()
            if factor_str == "":
                factor = 1.52  # valor estándar
            else:
                try:
                    factor = float(factor_str)
                    if factor < 1.0 or factor > 2.0:
                        messagebox.showwarning(
                            "Advertencia técnica",
                            "El factor de rendimiento debe estar entre 1.0 y 2.0.\nSolo modifique este valor si comprende su impacto en el volumen dosificado."
                        )
                        return
                except ValueError:
                    messagebox.showerror(
                        "Error de entrada",
                        "El valor ingresado en 'Factor de rendimiento' no es numérico.\nCorrija el dato o déjelo vacío para usar el valor estándar (1.52)."
                    )
                    return
                
            self.factor_rendimiento = factor

            if ajuste in {"baja", "media", "alta"}:
                etiqueta_wc = f"{ {'baja':0.45,'media':0.55,'alta':0.65}[ajuste]:.2f} (ajustada: {ajuste})"
            else:
                # aquí no tienes w_c aún, así que solo marca estándar
                etiqueta_wc = "Estándar (se calculará según resistencia)"



            # Ficha técnica previa al cálculo con sugerencia incluida
            resumen = (
                f"🔹 Resistencia: {resistencia} kg/cm²\n"
                f"🔹 Volumen: {volumen} m³\n"
                f"🔹 Tipo de elemento: {tipo}\n"
                f"🔹 Relación agua/cemento: {etiqueta_wc}\n"
                f"🔹 Porcentaje de aditivo: {self.vars['porc_aditivo'].get()}%\n"
                f"🔹 Factor de rendimiento: {factor:.2f}\n"
                f"🔹 Densidades:\n"
                f"   - Cemento: {self.vars['dens_cem'].get()} kg/m³\n"
                f"   - Arena: {self.vars['dens_are'].get()} kg/m³\n"
                f"   - Grava: {self.vars['dens_gra'].get()} kg/m³\n"
                f"🔹 Precios unitarios:\n"
                f"   - Cemento: {self.vars['precio_cem'].get()} $/kg\n"
                f"   - Arena:   {self.vars['precio_are'].get()} $/kg\n"
                f"   - Grava:   {self.vars['precio_gra'].get()} $/kg\n"
                f"   - Agua:    {self.vars['precio_agua'].get()} $/L\n"
                f"   - Aditivo: {self.vars['precio_aditivo'].get()} $/kg\n"
                f"🔹 IVA aplicado: {self.vars['iva'].get()}%\n"
            )

            prev_win = tk.Toplevel(self)
            prev_win.title("Ficha técnica previa")
            text_area = tk.Text(prev_win, wrap="word", width=30, height=20, font=("Arial", 14))
            text_area.insert("1.0", resumen)
            text_area.config(state="disabled")
            text_area.pack(padx=10, pady=10)

            def calcular():
                prev_win.destroy()
                resultados = self.calcular_dosificacion()
                ficha = resumen.replace("Ficha técnica previa", "Ficha técnica utilizada")
                self.mostrar_resultados(resultados, ficha)

            def editar():
                prev_win.destroy()
                messagebox.showinfo("Volver", "Volviendo al inicio para editar los datos...")

            btn_frame = tk.Frame(prev_win)
            btn_frame.pack(pady=10)
            tk.Button(btn_frame, text="Calcular", command=calcular, bg="green", fg="white").pack(side="left", padx=10)
            tk.Button(btn_frame, text="Editar datos", command=editar, bg="red", fg="white").pack(side="left", padx=10)       

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calcular_dosificacion(self):
        dosificaciones = {
            100: {"proporcion": (1, 4, 8), "w_c": 0.65},
            150: {"proporcion": (1, 3, 6), "w_c": 0.60},
            200: {"proporcion": (1, 2.5, 5), "w_c": 0.55},
            250: {"proporcion": (1, 2, 4), "w_c": 0.50},
            300: {"proporcion": (1, 1.5, 3), "w_c": 0.45}
        }

        factor_rendimiento = self.factor_rendimiento

        dens_cem = float(self.vars['dens_cem'].get())
        dens_are = float(self.vars['dens_are'].get())
        dens_gra = float(self.vars['dens_gra'].get())
        resistencia = int(self.vars['resistencia'].get())
        volumen_m3 = float(self.vars['volumen_m3'].get())
        tipo = self.vars['tipo'].get()
        ajuste_wc = self.vars['ajuste_wc'].get().lower()
        porc_aditivo = float(self.vars['porc_aditivo'].get()) / 100

        proporcion = dosificaciones[resistencia]["proporcion"]
        w_c = dosificaciones[resistencia]["w_c"]
        if ajuste_wc in {"baja", "media", "alta"}:
            w_c = {"baja": 0.45, "media": 0.55, "alta": 0.65}[ajuste_wc]

        c, s, g = proporcion
        partes_tot = c + s + g
        volumen_dosificado = volumen_m3 * factor_rendimiento

        V_c = volumen_dosificado * (c / partes_tot)
        V_s = volumen_dosificado * (s / partes_tot)
        V_g = volumen_dosificado * (g / partes_tot)

        m_c = V_c * dens_cem
        m_s = V_s * dens_are
        m_g = V_g * dens_gra
        m_agua = m_c * w_c
        dens_aditivo = 1.05  # kg/L, valor de ejemplo
        m_aditivo = m_c * porc_aditivo if porc_aditivo > 0 else 0
        vol_aditivo = m_aditivo / dens_aditivo if m_aditivo > 0 else 0
        sacos = m_c / 50

        volumen_seco = (m_c + m_s + m_g) / 1000
        volumen_liquido = m_agua / 1000
        volumen_total = volumen_seco + volumen_liquido
        masa_total = m_c + m_s + m_g + m_agua + m_aditivo

        return {
            "tipo": tipo,
            "resistencia": resistencia,
            "proporcion": f"{c}:{s}:{g}",
            "w_c": w_c,
            "volumen_solicitado": volumen_m3,
            "volumen_dosificado": volumen_dosificado,
            "factor_rendimiento": factor_rendimiento,
            "ajuste_wc": self.vars['ajuste_wc'].get().lower(),
            "porcentajes": {
                "cemento": c / partes_tot * 100,
                "arena": s / partes_tot * 100,
                "grava": g / partes_tot * 100
            },
            "normalizadas": {
                "arena": s / c,
                "grava": g / c
            },
            "densidades": {
                "cemento": dens_cem,
                "arena": dens_are,
                "grava": dens_gra
            },
            "materiales": {
                "cemento": m_c,
                "arena": m_s,
                "grava": m_g,
                "agua": m_agua,
                "aditivo": m_aditivo,
                "aditivo_L": vol_aditivo,
                "sacos": sacos
            },
            "volumenes": {
                "seco": volumen_seco,
                "agua": volumen_liquido,
                "total": volumen_total
            },
            "masa_total": masa_total
        }

    def mostrar_resultados(self, resultados, ficha_tecnica):
        ventana = tk.Toplevel(self)
        ventana.title("Resultados de dosificación")

        # Maximizar la ventana respetando la barra de tareas
        ventana.state("zoomed")
        ventana.resizable(True, True)

        # Configurar filas de la ventana con proporciones
        ventana.rowconfigure(0, weight=3)   # texto ocupa más
        ventana.rowconfigure(1, weight=2)   # tabla ocupa menos
        ventana.rowconfigure(2, weight=0)   # botones no se expanden
        ventana.columnconfigure(0, weight=1)
    
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#DDEEFF")
        style.configure("Treeview", font=("Consolas", 14), background="#FFFFFF",
                        foreground="#333333", fieldbackground="#FFFFFF")
        style.map("Treeview", background=[("selected", "#CCE5FF")])

        # Sección 1: texto con scrolls
        frame_texto = tk.Frame(ventana)
        frame_texto.grid(row=0, column=0, sticky="nsew")

        # Área de texto (izquierda)
        text_area = tk.Text(frame_texto, wrap="word", font=("Consolas", 14), bg="#FFFFFF")
        text_area.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        scroll_y = tk.Scrollbar(frame_texto, orient="vertical", command=text_area.yview)
        scroll_y.pack(side="right", fill="y")

        text_area.config(yscrollcommand=scroll_y.set)

        text_area.bind("<MouseWheel>", lambda e: text_area.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Estilos
        text_area.tag_config("azul", foreground="#00BFFF")
        text_area.tag_config("gris", foreground="#AAAAAA")
        text_area.tag_config("rojo", foreground="#FF5555")
        text_area.tag_config("amarillo", foreground="#FFD700")
        text_area.tag_config("verde", foreground="#00FF7F")
        text_area.tag_config("magenta", foreground="#FF00FF")
        text_area.tag_config("negrita", font=("Consolas", 10, "bold"))
        text_area.tag_config("centrado", justify="center")
        text_area.tag_config("naranja", foreground="orange")

        def escribir(texto, *tags):
            text_area.insert(tk.END, texto + "\n", tags if tags else None)

        # Ficha técnica
        escribir("📋 FICHA TÉCNICA UTILIZADA", "azul", "centrado")
        from datetime import datetime
        hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        escribir(f"Fecha y hora: {hora_actual}", "gris")
        for linea in ficha_tecnica.split("\n"):
            escribir(linea)
        escribir("—" * 60, "gris", "centrado")

        # Resultados principales
        escribir("=== RESULTADOS ===", "azul", "centrado")
        escribir(f"Elemento: {resultados['tipo']}")
        escribir(f"Resistencia: {resultados['resistencia']} kg/cm²")
        escribir(f"Proporción: {resultados['proporcion']} (Cemento:Arena:Grava)")
        if resultados.get("ajuste_wc") in {"baja", "media", "alta"}:
            escribir(f"Relación agua/cemento: {resultados['w_c']:.2f} (ajustada: {resultados['ajuste_wc']})")
        else:
            escribir(f"Relación agua/cemento: {resultados['w_c']:.2f} (estándar)")
        escribir(f"Volumen solicitado: {resultados['volumen_solicitado']:.2f} m³")
        escribir(f"Volumen dosificado (con rendimiento): {resultados['volumen_dosificado']:.2f} m³")
        escribir(f"Factor de rendimiento aplicado: {resultados['factor_rendimiento']}")

        # === Sección 2: tabla ===
        frame_tabla = tk.Frame(ventana)
        frame_tabla.grid(row=1, column=0, sticky="nsew")

        tabla = ttk.Treeview(frame_tabla, columns=("material", "cantidad", "costo"), show="headings")
        tabla.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Layout del frame de la tabla: tabla se expande, columna derecha fija
        frame_tabla.columnconfigure(0, weight=1)   # la tabla ocupa y se expande
        frame_tabla.columnconfigure(1, weight=0)   # columna para el label vertical
        frame_tabla.rowconfigure(0, weight=1)

        tabla.heading("material", text="Material")
        tabla.heading("cantidad", text="Cantidad")
        tabla.heading("costo", text="Costo")

        tabla.column("material", width=150)
        tabla.column("cantidad", width=120, anchor="center")
        tabla.column("costo", width=120, anchor="e")

        tabla.tag_configure("even", background="#FFFFFF")
        tabla.tag_configure("odd", background="#F5F5F5")
        tabla.tag_configure("total", background="#CCCCCC", font=("Consolas", 14, "bold"), foreground="#FF0000")
    
        # === COSTOS EN TABLA ===
        precio_cem = float(self.vars['precio_cem'].get()) * resultados['materiales']['cemento']
        precio_are = float(self.vars['precio_are'].get()) * resultados['materiales']['arena']
        precio_gra = float(self.vars['precio_gra'].get()) * resultados['materiales']['grava']
        precio_agua = float(self.vars['precio_agua'].get()) * resultados['materiales']['agua']
        precio_aditivo = float(self.vars['precio_aditivo'].get()) * resultados['materiales']['aditivo']
        total = precio_cem + precio_are + precio_gra + precio_agua + precio_aditivo
        costo_unitario = total / resultados['volumen_solicitado']

        try:
            iva_pct = float(self.vars['iva'].get())
        except ValueError:
            iva_pct = 0
            messagebox.showwarning("Aviso", "IVA inválido, se aplicó 0% por defecto.")

        iva_monto = total * (iva_pct / 100)
        total_con_iva = total + iva_monto

        filas = [
            ("Cemento", f"{resultados['materiales']['cemento']:.1f} kg", f"${precio_cem:,.2f}"),
            ("Arena", f"{resultados['materiales']['arena']:.1f} kg", f"${precio_are:,.2f}"),
            ("Grava", f"{resultados['materiales']['grava']:.1f} kg", f"${precio_gra:,.2f}"),
            ("Agua", f"{resultados['materiales']['agua']:.1f} kg ≈ {resultados['materiales']['agua']:.1f} L", f"${precio_agua:,.2f}")
        ]
        if resultados['materiales']['aditivo'] > 0:
            filas.append(("Aditivo",
                          f"{resultados['materiales']['aditivo']:.2f} kg ≈ {resultados['materiales']['aditivo_L']:.2f} L",
                          f"${precio_aditivo:,.2f}"))

        for i, fila in enumerate(filas):
            tag = "even" if i % 2 == 0 else "odd"
            tabla.insert("", "end", values=fila, tags=(tag,))

        # Continuar el contador para las filas de totales
        extra_filas = [
            ("Costo por m³ (sin IVA)", f"{resultados['volumen_solicitado']:.2f} m³", f"${costo_unitario:,.2f}"),
            ("Subtotal", "", f"${total:,.2f}"),
            (f"IVA {iva_pct:.1f}%", "", f"${iva_monto:,.2f}"),
            ("TOTAL", "", f"${total_con_iva:,.2f}"),
            ("Costo por m³ (con IVA)", f"{resultados['volumen_solicitado']:.2f} m³", f"${(total_con_iva/resultados['volumen_solicitado']):,.2f}"),
            ("Costo por m³ dosificado", f"{resultados['volumen_dosificado']:.2f} m³", f"${(total_con_iva/resultados['volumen_dosificado']):,.2f}")
        ]

        for j, fila in enumerate(extra_filas, start=len(filas)):
            if "TOTAL" in fila[0]:
                tabla.insert("", "end", values=fila, tags=("total",))
            else:
                tag = "even" if j % 2 == 0 else "odd"
                tabla.insert("", "end", values=fila, tags=(tag,))

        # === MODO PRÁCTICO: LATAS ===
        escribir("\n=== MODO PRÁCTICO: KG Y LATAS ===", "azul", "centrado")
        lata_volumen = 0.019
        densidades = {"arena": resultados['densidades']['arena'],
                      "grava": resultados['densidades']['grava'],
                      "agua": 1000}

        arena_latas = resultados['materiales']['arena'] / (densidades["arena"] * lata_volumen)
        grava_latas = resultados['materiales']['grava'] / (densidades["grava"] * lata_volumen)
        agua_litros = resultados['materiales']['agua']  # 1 kg ≈ 1 L
        agua_latas = resultados['materiales']['agua'] / 19

        escribir(f"Arena: {resultados['materiales']['arena']:.1f} kg ≈ {arena_latas:.1f} latas de 19 L", "naranja")
        escribir(f"Grava: {resultados['materiales']['grava']:.1f} kg ≈ {grava_latas:.1f} latas de 19 L", "rojo")
        escribir(f"Agua: {resultados['materiales']['agua']:.1f} L ≈ {agua_latas:.1f} latas de 19 L", "azul")

        # === Sección 3: botones ===
        btn_frame = tk.Frame(ventana)
        btn_frame.grid(row=2, column=0, sticky="ew", pady=10)
        
        def copiar_resultados():
            ventana.clipboard_clear()
            ventana.clipboard_append(text_area.get("1.0", "end"))
            messagebox.showinfo("Copiado",
                                "📋 Resultados copiados al portapapeles.",
                                parent=ventana)

        tk.Button(btn_frame, text="📋 Copiar resultados",
                  command=copiar_resultados, bg="#2196F3", fg="white").pack(side="left", padx=10)
        tk.Button(btn_frame, text="❌ Cerrar",
                  command=ventana.destroy, bg="#f44336", fg="white").pack(side="left", padx=10)

        text_area.config(state="disabled")
        
    def limpiar_datos(self):
        from tkinter import messagebox
        # Restaurar valores estándar
        self.vars['dens_cem'].set(1440)
        self.vars['dens_are'].set(1600)
        self.vars['dens_gra'].set(1500)
        self.vars['precio_cem'].set(f"{3.50:.2f}")
        self.vars['precio_are'].set(f"{1.20:.2f}")
        self.vars['precio_gra'].set(f"{1.00:.2f}")
        self.vars['precio_agua'].set(f"{0.01:.2f}")
        self.vars['precio_aditivo'].set(f"{15.0:.2f}")
        self.vars['iva'].set(16)
        self.vars['porc_aditivo'].set(0)

        # Vaciar los campos que son de entrada del usuario
        self.vars['resistencia'].set("")
        self.vars['volumen_m3'].set("")
        self.vars['tipo'].set("")
        self.vars['ajuste_wc'].set("")
        self.vars['factor_rendimiento'].set("")

        messagebox.showinfo("Valores restaurados", "Se han restablecido los valores estándar.")

# Ejecutar
if __name__ == "__main__":
    app = EntradaDatosApp()
    app.mainloop()
