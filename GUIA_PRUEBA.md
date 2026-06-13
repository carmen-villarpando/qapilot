# 🎮 Guía de Prueba QAPilot en GitHub UI

Guía paso a paso para probar QAPilot directamente en la interfaz de GitHub.

## 🚀 **Paso 1: Ir al Repositorio**

**URL:** `https://github.com/carmen-villarpando/qapilot`

## 📝 **Paso 2: Crear un Issue**

1. **Click en "Issues"** (barra superior del repositorio)
2. **Click en "New issue"** (botón verde)
3. **Completar el issue:**
   - **Title**: `el scroll no funciona en el dashboard`
   - **Description**: (déjalo vacío o pon algo simple)
   - **Labels**: (no selecciones nada)
4. **Click en "Submit new issue"**

## 💬 **Paso 3: Activar QAPilot**

1. **En el issue recién creado**, busca la sección de comentarios
2. **Escribe el comando:**
   ```
   /improve-issue
   ```
3. **Click en "Comment"**

## ⏱️ **Paso 4: Esperar la Magia**

### **Qué Verás Suceder:**

**🔥 Inmediato (1-5 segundos):**
- QAPilot agregará un 👍 reaction a tu comentario

**⚡ Procesamiento (30-60 segundos):**
- Ve a la pestaña **"Actions"** del repositorio
- Verás el workflow **"Improve Issue with QAPilot"** ejecutándose
- El workflow mostrará: `⏳ Running` → `✅ Success`

**🎉 Resultado (1-2 minutos total):**
- El issue se actualizará automáticamente con:
  - 📝 **Descripción detallada**
  - 🔧 **Pasos de reproducción**
  - ✅ **Comportamiento esperado**
  - 🏷️ **Labels sugeridos**
  - 📊 **Prioridad y assignee**

## 🔍 **Paso 5: Verificar el Resultado**

**El issue ahora contendrá:**

```markdown
## 📝 Description
El scroll vertical del dashboard principal no responde cuando el usuario intenta navegar por más de 10 elementos. Esto afecta principalmente a usuarios con pantallas más pequeñas donde el contenido excede el área visible...

## 🔧 Reproduction Steps
1. Iniciar sesión en la aplicación
2. Navegar al dashboard principal
3. Intentar hacer scroll hacia abajo
4. Observar que el scroll está congelado o no responde

## ✅ Expected Behavior
El usuario debería poder desplazarse suavemente por todo el contenido del dashboard utilizando la rueda del mouse, trackpad o scroll en dispositivos táctiles...

## 📊 Metadata
**Priority:** medium
**Suggested Assignee:** frontend-team
```

## 🎯 **Paso 6: Ver el Comentario de Confirmación**

QAPilot agregará un comentario como:
```
🚀 **Issue improved by QAPilot!**

Triggered by @tu-usuario
Added description, reproduction steps, expected behavior, and labels.
```

## ⚠️ **Si No Funciona**

### **Revisa GitHub Actions:**
1. Ve a: `https://github.com/carmen-villarpando/qapilot/actions`
2. Busca el workflow más reciente
3. Si está en rojo ❌, click para ver los logs

### **Posibles Problemas:**
- **GitHub Actions no habilitados**: Ve a Settings → Actions
- **Secrets incorrectos**: Revisa QAPILOT_GITHUB_TOKEN y QAPILOT_MODELS_TOKEN
- **Permisos insuficientes**: El token necesita scopes `repo` y `workflow`

## 🎪 **Para Demo de Hackathon**

**Script Sugerido:**

> "Miren este issue con título simple: 'el scroll no funciona'. Ahora voy a mejorarlos con QAPilot."
> 
> *(Comenta `/improve-issue`)*
> 
> "Vean cómo QAPilot automáticamente agrega descripción detallada, pasos de reproducción, y labels. Todo en segundos, gratis, y sin salir de GitHub."

## 🔄 **Probar con Otros Ejemplos**

**Títulos de prueba:**
- `el login no funciona`
- `error 500 al guardar`
- `botón de submit deshabilitado`
- `no puedo exportar datos`

**Cada uno generará mejoras diferentes basadas en el contexto.**

---

## 🎯 **Checklist Final**

- [ ] Issue creado con título simple
- [ ] Comentario `/improve-issue` agregado
- [ ] GitHub Action ejecutándose
- [ ] Issue actualizado con contenido enriquecido
- [ ] Comentario de confirmación visible

**¡QAPilot está funcionando! 🎉**
