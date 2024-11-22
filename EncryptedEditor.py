from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import curses


key = b'1234567890abcdef' 
iv = b'abcdef9876543210'   

# Funcion de encriptación
def encriptar(texto):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    texto_padded = pad(texto.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(texto_padded)
    return ciphertext

# Funcion de desencriptación
def desencriptar(ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext_padded = cipher.decrypt(ciphertext)
    return unpad(plaintext_padded, AES.block_size).decode('utf-8')

# Funcion para guardar texto encriptado
def guardar_encriptado(nombre_archivo, texto):
    cipher = encriptar(texto)
    with open(nombre_archivo, 'wb') as archivo:
        archivo.write(iv)  
        archivo.write(cipher)

# Funcion para cargar texto desencriptado
def cargar_desencriptado(nombre_archivo):
    with open(nombre_archivo, 'rb') as archivo:
        iv_leido = archivo.read(16)  
        cipher = archivo.read()      
        return desencriptar(cipher)

# Función para usar curses
def interactuar_con_usuario(stdscr):
    curses.curs_set(1)
    stdscr.clear()

    nombre_archivo = "archivo_encriptado.bin"
    try:
        contenido = cargar_desencriptado(nombre_archivo)
    except Exception as e:
        contenido = ""
        stdscr.addstr(0, 0, "No se pudo desencriptar el archivo, se creará uno nuevo.\n")

    
    stdscr.addstr(1, 0, "Contenido desencriptado del archivo:\n")
    stdscr.addstr(2, 0, contenido.replace("\n", " "))

    
    stdscr.addstr(4, 0, "\n--- Escribe el nuevo contenido (presiona Ctrl+D para guardar, Backspace para borrar) ---\n")
    stdscr.refresh()

    nuevo_contenido = ""
    while True:
        ch = stdscr.getch()
        if ch == 4:  # Ctrl+D
            break
        elif ch == 10:  # Nueva línea
            nuevo_contenido += '\n'
            stdscr.addstr("\n")
        elif ch == 263:  # Backspace (Tecla de borrar)
            if len(nuevo_contenido) > 0:
                nuevo_contenido = nuevo_contenido[:-1]  
                stdscr.clear()  
                stdscr.addstr(1, 0, "Contenido desencriptado del archivo:\n")
                stdscr.addstr(2, 0, contenido.replace("\n", " ")) 
                stdscr.addstr(4, 0, "\n--- Escribe el nuevo contenido (presiona Ctrl+D para guardar, Backspace para borrar) ---\n")
                stdscr.addstr(nuevo_contenido) 
        else:
            nuevo_contenido += chr(ch)
            stdscr.addstr(chr(ch))

    contenido += "\n" + nuevo_contenido

    
    guardar_encriptado(nombre_archivo, contenido)
    stdscr.addstr("\nArchivo guardado exitosamente encriptado.")
    stdscr.refresh()
    stdscr.getch()

def main():
    curses.wrapper(interactuar_con_usuario)

if __name__ == "__main__":
    main()
