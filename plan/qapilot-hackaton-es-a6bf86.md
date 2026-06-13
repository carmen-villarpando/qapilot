# Plan QAPilot Hackathon (Español)

Crear una herramienta de mejora de issues de GitHub que utiliza los modelos gratuitos de GitHub para mejorar automáticamente la calidad de los tickets analizando títulos simples y generando descripciones completas, etiquetas y metadatos cuando el usuario lo activa manualmente.

## Requisitos Confirmados

1. **Mecanismo de Activación**: Manual mediante comentario en GitHub UI (`/improve-issue`)
2. **Modelo**: GitHub Models API (gratuito) - menor consumo de recursos
3. **Alcance**: Repositorios personales únicamente
4. **Salida**: Actualización directa del ticket después de que el usuario actualiza el título
5. **Interfaz**: 100% dentro de GitHub UI, sin aplicaciones externas

## Investigación de Mercado

Herramientas similares existen:
- **GitHub Copilot**: Auto-completa issues pero requiere suscripción pagada
- **Linear AI**: Gestión de issues con IA (plataforma separada)
- **Sentry Issues**: Auto-genera detalles de issues (enfocado en errores)
- **IssueOps**: GitHub Action para automatización de issues (IA limitada)

**Nuestro Diferenciador**: Gratuito, nativo de GitHub, usa modelos propios de GitHub, control manual del usuario.

## Plan de Implementación

### Fase 1: Infraestructura Base
- Configurar estructura de proyecto uv con pyproject.toml
- Implementar cliente GitHub API usando PyGithub
- Crear cliente GitHub Models API
- Diseñar plantillas de prompts para análisis de issues
- Configurar GitHub Actions workflow

### Fase 2: Sistema de Activación Manual
- Implementar activación por comentario (`/improve-issue`)
- Crear manejador de eventos issue_comment en GitHub Action
- Agregar validación de permisos y controles
- Construir mecanismo de respuesta en GitHub UI

### Fase 3: Lógica de Negocio
- Construir issue_improver.py con integración GitHub Models
- Crear formato de salida estructurado (descripción, etiquetas, prioridad, pasos de reproducción)
- Agregar manejo de errores y feedback al usuario
- Implementar actualización directa de issue después del cambio de título

### Fase 4: Integración y Pruebas
- Configurar secrets de API de GitHub Models
- Agregar logging y monitoreo
- Crear suite de pruebas con datos de prueba
- Desplegar en repositorio personal

## Stack Técnico
- **Gestor de Paquetes**: uv
- **LLM**: GitHub Models API (tier gratuito)
- **GitHub API**: PyGithub
- **Activación**: Eventos de comentarios de issues
- **Despliegue**: GitHub Actions (hosteado por GitHub)

## Flujo de Usuario
1. Usuario crea issue con título simple
2. Usuario agrega comentario: `/improve-issue`
3. GitHub Action se activa, analiza título con GitHub Models
4. Script actualiza issue con detalles completos
5. Usuario ve issue mejorado en la misma interfaz de GitHub

## Criterios de Éxito
- Activación manual funciona via comando de comentario
- GitHub Models API provee sugerencias de calidad
- Actualizaciones directas de issues sin salir de GitHub
- Funciona en repositorios personales
- Uso de tier gratuito dentro de límites
