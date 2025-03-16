# agents-payretailers

## Inspiration
Hoy en día, hay ciertas comunidades en LATAM que requieren de mejoras en accesibilidad i mejora de vida global. Los recientes avances de la IA y agentes han permitido llenar el vacío y solucionar varios problemas. Hemos creado un servicio que ayuda a la población de Latino America tener acceso a recursos legales, simplificar trámites i acceder a información esencial de una manera fácil de usar.
## What it does
Nuestra aplicación puede acceder a bases de datos gubernamentales y de estadísticas económicas y demográficas de países de Latino America. También, esta diseñada para ejecutar acciones en un buscador (por ejemplo, obtener ayuda al rellenar formularios para renovar pasaportes u obtener datos en tiempo real de los buses i transportes).
## How we built it
Hemos diseñado un sistema multi-agente que puede ejecutar multiples acciones utilizando bases de datos, APIs, LLMs i buscadores web automatizados. Para desarrollarlo hemos empezado tres pasos:
1. Hacer que el agente descubra que estadísticas destacar utilizando similaridad de vectores (embeddings)
2. Una vez se obtiene la estadística, recibimos parámetros que el agente tiene que averiguar, como el país, el año o el sexo.
3. El agente averigua el país y otros parámetros o bien por la memoria o por input del usuario por lenguaje natural, después el agente obtiene estos datos y retorna las estadísticas de forma detallada.
## Challenges we ran into
Flowise era demasiado de alto nivel, necesitábamos tener mas control sobre cada modulo de nuestro sistema multiagente. Por esa razón, hemos programado nosotros mismos el workflow entero.
## Accomplishments that we're proud of
Estamos muy orgullosos de nuestro progreso en sistemas multiagente, un campo que no habíamos explorado y que nos ha parecido fascinante. Diseñar agentes que colaboran, realizan tareas intercaladas y usan LLMs para cumplir objetivos ha sido un desafío emocionante. Además, integrar Retrieval Augmented Generation (RAG) nos ha permitido mejorar la toma de decisiones basada en IA.

También hemos desarrollado aplicaciones web con Flask y mejorado nuestra interacción con APIs, permitiéndonos conectar con modelos en la nube como GPT-4o-mini y acceder a grandes bases de datos, especialmente en América Latina. Esta experiencia ha fortalecido nuestras habilidades técnicas y nuestra capacidad para crear soluciones de IA con datos del mundo real.

Y sobretodo, hemos reforzado nuestras habilidades de trabajo en equipo!
## What we learned
Hemos aprendido a diseñar y coordinar sistemas multiagente, explorando cómo los agentes pueden colaborar, ejecutar tareas intercaladas y utilizar LLMs para resolver problemas de manera eficiente. También hemos integrado Retrieval Augmented Generation (RAG), lo que nos ha permitido mejorar la toma de decisiones al proporcionar información relevante al modelo en tiempo real.

Además, hemos adquirido habilidades en el desarrollo de aplicaciones web con Flask y en la interacción con APIs, conectando modelos en la nube como GPT-4o-mini y accediendo a grandes bases de datos, especialmente en América Latina. Esto nos ha dado una comprensión más profunda de la integración entre IA y datos externos.

## What's next for Better Life
Nuestro siguiente paso es optimizar la interfaz para ofrecer una experiencia de usuario más intuitiva y accesible. Además, realizaremos un fine-tunning de nuestros agentes, lo que les permitirá aprender y adaptarse de manera más precisa a las necesidades de cada tarea. Este proceso no solo mejorará la eficacia de las interacciones, sino que también fortalecerá la integración con otros sistemas y recursos, llevando nuestra solución a un nuevo nivel de rendimiento y utilidad para la comunidad.
