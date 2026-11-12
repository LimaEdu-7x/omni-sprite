# Catálogo de ferramentas do pixel-mcp (v0.5.0)

Leia sempre o schema de entrada atual de cada ferramenta antes da primeira chamada; os nomes abaixo vêm do README do projeto e foram conferidos com a lista de 50 ferramentas do servidor.

- **Tela/camadas:** `create_canvas`, `add_layer`, `delete_layer`, `flatten_layers`, `get_sprite_info`
- **Desenho:** `draw_pixels` (lote, ajuste à paleta), `draw_line`, `draw_contour`, `draw_rectangle`, `draw_circle`, `fill_area`
- **Seleção:** `select_rectangle`, `select_ellipse`, `select_all`, `deselect`, `move_selection`, `cut_selection`, `copy_selection`, `paste_clipboard`
- **Pixel art avançado:** `analyze_reference`, `draw_with_dither` (Bayer, Floyd-Steinberg, texturas…), `downsample_image`, `get_palette`, `set_palette`, `set_palette_color`, `add_palette_color`, `sort_palette`, `apply_shading` (smooth/hard/pillow, 8 direções de luz), `analyze_palette_harmonies`, `suggest_antialiasing`
- **Transformação:** `flip_sprite`, `rotate_sprite` (90/180/270), `scale_sprite` (nearest/bilinear/rotsprite), `crop_sprite`, `resize_canvas`, `apply_outline`
- **Animação:** `add_frame`, `delete_frame`, `set_frame_duration`, `create_tag`, `delete_tag`, `duplicate_frame`, `link_cel`
- **Entrada/saída:** `get_pixels` (paginado), `export_sprite` (PNG/GIF/JPG/BMP), `export_spritesheet` (+JSON), `import_image`, `save_as`

Regras práticas: modo de cor indexado para trabalhar com paleta; `rotsprite` para girar pixel art; `nearest` para ampliar prévias; confira com `get_pixels` em regiões pequenas em vez de adivinhar.
