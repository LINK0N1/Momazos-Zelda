import io
import os
import urllib.request
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Configuración visual de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class MemeGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Meme Generator App - Python Senior Edition")
        self.geometry("1100x750")
        self.minsize(900, 600)

        # Estado de la imagen y canvas
        self.original_image = None
        self.display_image = None
        self.tk_image = None
        self.scale_factor = 1.0

        # Estilos de texto
        self.font_size = 40
        self.text_color = "#FFFFFF"
        self.stroke_color = "#000000"

        # Posiciones del texto en coordenadas de la imagen original (x, y)
        self.top_text_pos = [0, 0]
        self.bottom_text_pos = [0, 0]

        # Elementos arrastrables en el Canvas ("top", "bottom" o None)
        self.drag_data = {"item": None, "x": 0, "y": 0}

        self._build_ui()

    def _build_ui(self):
        # Layout Principal: Controles (Izquierda) y Preview (Derecha)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- Panel de Controles (Izquierda) ----------------
        self.sidebar = ctk.CTkScrollableFrame(self, width=350, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Sección 1: Carga de Imagen
        ctk.CTkLabel(self.sidebar, text="1. Fuente de la Imagen", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(10, 5))

        self.url_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Pega la URL de una imagen...")
        self.url_entry.pack(fill="x", pady=5)

        btn_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        btn_frame.pack(fill="x", pady=5)
        ctk.CTkButton(btn_frame, text="Cargar URL", command=self.load_image_from_url, width=150).pack(side="left", padx=(0, 5))
        ctk.CTkButton(btn_frame, text="Archivo Local", command=self.load_image_from_file, width=150).pack(side="right")

        # Sección 2: Textos del Meme
        ctk.CTkLabel(self.sidebar, text="2. Textos del Meme", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(15, 5))

        self.top_text_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Texto Superior (Top Text)")
        self.top_text_entry.pack(fill="x", pady=5)
        self.top_text_entry.bind("<KeyRelease>", lambda e: self.render_meme())

        self.bottom_text_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Texto Inferior (Bottom Text)")
        self.bottom_text_entry.pack(fill="x", pady=5)
        self.bottom_text_entry.bind("<KeyRelease>", lambda e: self.render_meme())

        # Sección 3: Personalización de Estilo
        ctk.CTkLabel(self.sidebar, text="3. Estilo del Texto", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(15, 5))

        ctk.CTkLabel(self.sidebar, text="Tamaño de Fuente:").pack(anchor="w")
        self.font_slider = ctk.CTkSlider(self.sidebar, from_=10, to=120, number_of_steps=110, command=self._on_font_slider_change)
        self.font_slider.set(self.font_size)
        self.font_slider.pack(fill="x", pady=5)

        color_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        color_frame.pack(fill="x", pady=5)
        ctk.CTkButton(color_frame, text="Color Texto", command=self.choose_text_color, width=150).pack(side="left", padx=(0, 5))
        ctk.CTkButton(color_frame, text="Color Borde", command=self.choose_stroke_color, width=150).pack(side="right")

        # Sección 4: Acciones
        ctk.CTkLabel(self.sidebar, text="4. Acciones", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", pady=(15, 5))
        ctk.CTkButton(self.sidebar, text="Generar / Refrescar", command=self.render_meme, fg_color="green", hover_color="darkgreen").pack(fill="x", pady=5)
        ctk.CTkButton(self.sidebar, text="Exportar / Guardar", command=self.save_meme, fg_color="blue", hover_color="darkblue").pack(fill="x", pady=5)

        # ---------------- Panel de Previsualización (Derecha) ----------------
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.preview_frame.grid_rowconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.preview_frame, bg="#1e1e1e", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Bindings para el arrastre interactivo en Canvas
        self.canvas.bind("<ButtonPress-1>", self._on_drag_start)
        self.canvas.bind("<B1-Motion>", self._on_drag_motion)
        self.canvas.bind("<Configure>", self._on_canvas_resize)

    # ---------------- Carga y Manejo de Imágenes ----------------

    def load_image_from_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar Imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.webp")]
        )
        if file_path:
            try:
                img = Image.open(file_path).convert("RGB")
                self._set_new_image(img)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen local:\n{e}")

    def load_image_from_url(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Por favor ingresa una URL válida.")
            return

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read()
            img = Image.open(io.BytesIO(data)).convert("RGB")
            self._set_new_image(img)
        except Exception as e:
            messagebox.showerror("Error de Red", f"No se pudo descargar la imagen desde la URL:\n{e}")

    def _set_new_image(self, img):
        self.original_image = img
        w, h = img.size

        # Posiciones iniciales por defecto (arriba y abajo)
        self.top_text_pos = [w // 2, int(h * 0.1)]
        self.bottom_text_pos = [w // 2, int(h * 0.85)]

        self.render_meme()

    # ---------------- Lógica de Dibujado de Texto con Borde ----------------

    def _get_impact_font(self, size):
        """Intenta cargar la fuente Impact del sistema; usa una fuente por defecto si no existe."""
        font_names = ["impact.ttf", "Impact.ttf", "Impact", "arial.ttf", "Arial.ttf"]
        for name in font_names:
            try:
                return ImageFont.truetype(name, size)
            except IOError:
                continue
        return ImageFont.load_default()

    def _draw_text_with_stroke(self, draw, text, position, font, text_color, stroke_color, stroke_width):
        """Dibuja texto centrado con un contorno definido usando Pillow."""
        x, y = position
        
        # Calcular el bounding box para centrar el texto correctamente
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        draw_x = x - (text_w / 2)
        draw_y = y - (text_h / 2)

        # Dibujar el contorno trazando el texto en un patrón circular a la distancia del grosor
        for dx in range(-stroke_width, stroke_width + 1):
            for dy in range(-stroke_width, stroke_width + 1):
                if dx * dx + dy * dy <= stroke_width * stroke_width:
                    draw.text((draw_x + dx, draw_y + dy), text, font=font, fill=stroke_color)

        # Dibujar el texto principal en el centro
        draw.text((draw_x, draw_y), text, font=font, fill=text_color)

    def _generate_meme_image(self):
        """Genera la imagen completa con los textos aplicados a resolución original."""
        if self.original_image is None:
            return None

        meme = self.original_image.copy()
        draw = ImageDraw.Draw(meme)
        font = self._get_impact_font(self.font_size)
        stroke_w = max(2, int(self.font_size * 0.08))

        top_text = self.top_text_entry.get().upper()
        bottom_text = self.bottom_text_entry.get().upper()

        if top_text:
            self._draw_text_with_stroke(
                draw, top_text, tuple(self.top_text_pos),
                font, self.text_color, self.stroke_color, stroke_w
            )

        if bottom_text:
            self._draw_text_with_stroke(
                draw, bottom_text, tuple(self.bottom_text_pos),
                font, self.text_color, self.stroke_color, stroke_w
            )

        return meme

    # ---------------- Renderizado en Pantalla ----------------

    def render_meme(self):
        if self.original_image is None:
            return

        full_meme = self._generate_meme_image()
        if full_meme is None:
            return

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        if canvas_w <= 10 or canvas_h <= 10:
            return

        # Ajuste dinámico (Fit to Screen) manteniendo relación de aspecto
        img_w, img_h = full_meme.size
        self.scale_factor = min(canvas_w / img_w, canvas_h / img_h)

        new_w = int(img_w * self.scale_factor)
        new_h = int(img_h * self.scale_factor)

        resized_img = full_meme.resize((new_w, new_h), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized_img)

        # Centrar la imagen en el Canvas
        offset_x = (canvas_w - new_w) // 2
        offset_y = (canvas_h - new_h) // 2

        self.canvas.delete("all")
        self.canvas.create_image(offset_x, offset_y, anchor="nw", image=self.tk_image, tags="meme_img")

    # ---------------- Arrastre Interactivo (Drag & Drop) ----------------

    def _on_drag_start(self, event):
        if self.original_image is None:
            return

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        img_w, img_h = self.original_image.size

        offset_x = (canvas_w - (img_w * self.scale_factor)) / 2
        offset_y = (canvas_h - (img_h * self.scale_factor)) / 2

        # Convertir clic a coordenadas absolutas de la imagen original
        orig_click_x = (event.x - offset_x) / self.scale_factor
        orig_click_y = (event.y - offset_y) / self.scale_factor

        # Determinar si el clic fue cerca del texto superior o inferior
        dist_top = ((orig_click_x - self.top_text_pos[0])**2 + (orig_click_y - self.top_text_pos[1])**2)**0.5
        dist_bottom = ((orig_click_x - self.bottom_text_pos[0])**2 + (orig_click_y - self.bottom_text_pos[1])**2)**0.5

        threshold = (self.font_size * 2)
        if dist_top < dist_bottom and dist_top < threshold:
            self.drag_data["item"] = "top"
        elif dist_bottom < threshold:
            self.drag_data["item"] = "bottom"
        else:
            self.drag_data["item"] = None

    def _on_drag_motion(self, event):
        item = self.drag_data["item"]
        if not item or self.original_image is None:
            return

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        img_w, img_h = self.original_image.size

        offset_x = (canvas_w - (img_w * self.scale_factor)) / 2
        offset_y = (canvas_h - (img_h * self.scale_factor)) / 2

        # Mapear nueva posición a coordenadas de la imagen original
        new_orig_x = max(0, min(img_w, (event.x - offset_x) / self.scale_factor))
        new_orig_y = max(0, min(img_h, (event.y - offset_y) / self.scale_factor))

        if item == "top":
            self.top_text_pos = [int(new_orig_x), int(new_orig_y)]
        elif item == "bottom":
            self.bottom_text_pos = [int(new_orig_x), int(new_orig_y)]

        self.render_meme()

    # ---------------- Control de Eventos y Configuración ----------------

    def _on_font_slider_change(self, value):
        self.font_size = int(value)
        self.render_meme()

    def choose_text_color(self):
        color = colorchooser.askcolor(title="Seleccionar Color de Texto", initialcolor=self.text_color)
        if color[1]:
            self.text_color = color[1]
            self.render_meme()

    def choose_stroke_color(self):
        color = colorchooser.askcolor(title="Seleccionar Color del Borde", initialcolor=self.stroke_color)
        if color[1]:
            self.stroke_color = color[1]
            self.render_meme()

    def _on_canvas_resize(self, event):
        self.render_meme()

    def save_meme(self):
        if self.original_image is None:
            messagebox.showwarning("Aviso", "Carga una imagen antes de intentar exportar.")
            return

        final_meme = self._generate_meme_image()
        if final_meme is None:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")],
            title="Guardar Meme Como..."
        )

        if file_path:
            try:
                final_meme.save(file_path)
                messagebox.showinfo("Éxito", f"Meme guardado correctamente en:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar la imagen:\n{e}")


if __name__ == "__main__":
    app = MemeGeneratorApp()
    app.mainloop()