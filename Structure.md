pendulo-invertido/
│
├── backend/                # Backend en Python
│   ├── api/                # API para comunicación
│   │   ├── endpoints.py    # Definición de endpoints
│   │   ├── models.py       # Modelos de datos
│   │   ├── utils.py        # Funciones auxiliares
│   │   └── train.py        # Entrenamiento del agente
│   ├── requirements.txt    # Dependencias del backend
│   ├── app.py              # Entrada principal del backend
│   └── Dockerfile          # Dockerfile para backend
│
├── simulation/             # Simulador y control del péndulo
│   ├── cartpole_env.py     # Personalización de CartPole-v1
│   ├── q_learning.py       # Implementación de Q-Learning
│   ├── sarsa.py            # Implementación de SARSA
│   ├── dqn.py              # Implementación de DQN
│   └── policy_gradient.py  # Implementación de Policy Gradient
│
├── frontend/               # Interfaz React
│   ├── public/             # Archivos estáticos
│   ├── src/                # Código fuente
│   │   ├── components/     # Componentes de React
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Controls.jsx
│   │   │   └── Metrics.jsx
│   │   ├── App.jsx         # Componente principal
│   │   ├── index.js        # Entrada principal
│   │   └── styles.css      # Estilos
│   └── package.json        # Dependencias del frontend
│
├── deployment/             # Scripts de despliegue
│   ├── docker-compose.yml  # Configuración de Docker Compose
│   ├── setup.sh            # Script de inicialización en la VM
│   └── README.md           # Documentación de despliegue
│
├── tests/                  # Pruebas unitarias y de integración
│   ├── backend_tests.py    # Pruebas para el backend
│   └── simulation_tests.py # Pruebas para el simulador
│
├── README.md               # Documentación del proyecto
└── LICENSE                 # Licencia del proyecto
