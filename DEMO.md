# 🎭 QAPilot Demo Guide

Guía completa para configurar y demostrar QAPilot en hackathon o presentación.

## 🎯 **Demo de 5 Minutos**

### **Escenario del Problema**
"Los desarrolladores crean issues con títulos pobres como 'bug' o 'no funciona', perdiendo tiempo en aclaraciones."

### **Solución QAPilot**
QAPilot transforma automáticamente títulos simples en issues completos y profesionales.

---

## 🚀 **Configuración Paso a Paso (Para Demo)**

### **Paso 1: GitHub Secrets (2 minutos)**

Ve a: **https://github.com/carmen-villarpando/qapilot/settings/secrets/actions**

**1. GITHUB_TOKEN**
- Click "New repository secret"
- Name: `GITHUB_TOKEN`
- Value: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- *Obtener de: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)*

**2. GITHUB_MODELS_TOKEN**
- Click "New repository secret"
- Name: `GITHUB_MODELS_TOKEN`
- Value: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- *Obtener de: GitHub → Settings → Developer settings → GitHub Models*

### **Paso 2: Habilitar GitHub Actions (30 segundos)**

Ve a: **https://github.com/carmen-villarpando/qapilot/settings/actions**

- ✅ "Allow all actions"
- ✅ "Allow read and write permissions"

---

## 🎪 **Script de Demo**

### **Intro (30 segundos)**
> "Hoy presento QAPilot: la solución automática para mejorar issues de GitHub. ¿Alguna vez recibieron un issue que dice 'bug' y no saben qué hacer? QAPilot lo arregla automáticamente."

### **Demo Live (2 minutos)**

**1. Crear Issue**
```
Título: "el scroll no funciona"
```

**2. Activar QAPilot**
```
Comentario: /improve-issue
```

**3. Magia Automática**
- 🤖 QAPilot analiza el título
- 📝 Genera descripción detallada
- 🔧 Agrega pasos de reproducción
- ✅ Define comportamiento esperado
- 🏷️ Sugiere labels relevantes
- 📊 Asigna prioridad

### **Resultado Final**
```
## 📝 Description
El scroll vertical del dashboard principal no responde cuando el usuario intenta navegar por más de 10 elementos...

## 🔧 Reproduction Steps
1. Iniciar sesión en el dashboard
2. Navegar a la sección principal
3. Intentar hacer scroll hacia abajo
4. Observar que el scroll está congelado

## ✅ Expected Behavior
El usuario debería poder desplazarse suavemente por todo el contenido del dashboard...

## 📊 Metadata
**Priority:** medium
**Suggested Assignee:** frontend-team
```

---

## 💡 **Puntos Clave para Demo**

### **🎯 Problema Resuelto**
- **Antes**: Issues ambiguos → pérdida de tiempo
- **Después**: Issues completos → desarrollo eficiente

### **🚀 Beneficios**
- **100% Gratuito**: No hay costos ocultos
- **GitHub Native**: Sin apps externas
- **Control Manual**: El usuario decide cuándo usarlo
- **IA Potente**: GitHub Models API

### **� Análisis de Costos - 100% GRATIS**

| Servicio | Costo | Free Tier | Uso QAPilot | Margen |
|----------|-------|------------|-------------|---------|
| GitHub Actions | $0 | 2,000 min/mes | ~50 min/mes | 97.5% disponible |
| GitHub Models | $0 | Incluido | ~100 llamadas/mes | Generoso límite |
| GitHub API | $0 | 5,000 req/hora | ~300 req/mes | 94% disponible |
| **TOTAL** | **$0.00** | | | |

**🎯 Escenario Real (Uso Personal/Hackathon):**
```
Issues mejorados: 100/mes
Tiempo GitHub Actions: 50 minutos (de 2,000 gratis)
Llamadas Models API: 100 (dentro del free tier)
Requests GitHub API: 300 (de 5,000 por hora)

COSTO TOTAL: $0.00
```

**✅ Sin Costos Ocultos:**
- No requiere tarjeta de crédito
- No hay suscripción mensual
- No hay límites estrictos para uso personal
- No hay cargos por almacenamiento o transferencia

### **�🔧 Características Técnicas**
- **Stack**: Python + uv + GitHub Actions
- **Modelos**: Llama 3.1, Mistral (free tier)
- **Trigger**: Comentario `/improve-issue`
- **Integración**: Total dentro de GitHub UI

---

## 🎭 **Tips para Demo Exitosa**

### **Preparación**
1. **Tener tokens listos** antes de la demo
2. **Crear issue de prueba** previamente
3. **Verificar GitHub Actions** funcionando

### **Durante Demo**
1. **Mostrar el problema** con un issue real
2. **Explicar el trigger** `/improve-issue`
3. **Dejar que corra** el GitHub Action en vivo
4. **Mostrar el resultado** transformado

### **Cierre Fuerte**
> "QAPilot no solo mejora issues, mejora la productividad del equipo. En 30 segundos transformamos un issue ambiguo en una tarea clara y accionable. Todo gratis, todo dentro de GitHub."

---

## 🆚 **Comparativa con Competidores**

| Herramienta | Costo | Integración | Control |
|-------------|-------|-------------|---------|
| GitHub Copilot | $10/mes | GitHub | Automático |
| Linear AI | $8/mes | App separada | Manual |
| **QAPilot** | **$0** | **GitHub Native** | **Manual** |

---

## 🎯 **Call to Action**

> "Para implementar QAPilot en tu proyecto:
> 1. Fork este repositorio
> 2. Configura los secrets
> 3. Comienza a mejorar issues hoy mismo
> 
> ¡Todo en menos de 5 minutos y 100% gratis!"

---

## 🔗 **Recursos**

- **Repositorio**: https://github.com/carmen-villarpando/qapilot
- **Documentación**: README.md completo
- **Planes**: carpeta `plan/` con diseño técnico
- **Tests**: Suite completa validando funcionalidad

---

## 🎪 **FAQ Demo**

**¿Es realmente gratis?**
- Sí, GitHub Actions (2,000 min/mes) + GitHub Models (free tier) = $0

**¿Funciona con cualquier repositorio?**
- Sí, solo necesita configurar los secrets

**¿Qué pasa si no me gusta el resultado?**
- El trigger es manual, solo se usa cuando quieres

**¿Necesito instalar algo?**
- No, todo corre en GitHub, sin apps externas

---

**🚀 QAPilot: Transformando issues ambiguos en tareas claras, automáticamente.**
