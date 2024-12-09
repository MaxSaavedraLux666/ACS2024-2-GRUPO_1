import './Cartpole.css';
import { useState } from 'react';

function Cartpole() {
    const [showDescription, setShowDescription] = useState(null);

    const toggleDescription = (param) => {
        setShowDescription(showDescription === param ? null : param);
    };

    return (
        <div className="contentMain">
            {/* Navbar */}
            <div className="navbar">
                <span className="navbarTitle">Cart Pole</span>
                <span className="navbarItem">Nosotros</span>
            </div>

            {/* Parametros */}
            <div className="contentParameter">
                <div className="parameterBox">
                    <label>
                        Epsilon
                        <input type="number" name="epsilon" />
                        <button onClick={() => toggleDescription('epsilon')} className="helpButton">?</button>
                    </label>
                    <label>
                        Gamma
                        <input type="number" name="gamma" />
                        <button onClick={() => toggleDescription('gamma')} className="helpButton">?</button>
                    </label>
                    <label>
                        Masa de Carro
                        <input type="number" name="massCar" />
                        <button onClick={() => toggleDescription('massCar')} className="helpButton">?</button>
                    </label>
                    <label>
                        Longitud del Péndulo
                        <input type="number" name="pendulumLength" />
                        <button onClick={() => toggleDescription('pendulumLength')} className="helpButton">?</button>
                    </label>
                    <label>
                        Fuerza Máxima
                        <input type="number" name="maxForce" />
                        <button onClick={() => toggleDescription('maxForce')} className="helpButton">?</button>
                    </label>
                    <label>
                        Tasa de Aprendizaje
                        <input type="number" name="learningRate" />
                        <button onClick={() => toggleDescription('learningRate')} className="helpButton">?</button>
                    </label>
                </div>
            </div>

            {/* Simulador */}
            <div className="contentSimulator">
                <div className="carruselSimulator">
                    <div className="carouselItem">Simulación 1</div>
                    <div className="carouselItem">Simulación 2</div>
                    <button className="nextButton">Siguiente</button>
                </div>
                <div className="leyenda">
                    <h3>Descripción de los parámetros</h3>
                    <p>Haz clic en el signo de interrogación junto a los parámetros para más detalles.</p>
                    {showDescription === 'epsilon' && <div className="helpText">Epsilon controla la exploración del agente. Un valor alto significa más exploración.</div>}
                    {showDescription === 'gamma' && <div className="helpText">Gamma es el factor de descuento para el valor futuro de las recompensas.</div>}
                    {showDescription === 'massCar' && <div className="helpText">La masa del carro es un parámetro importante que influye en la dinámica del sistema.</div>}
                    {showDescription === 'pendulumLength' && <div className="helpText">La longitud del péndulo influye en la estabilidad y el comportamiento del sistema.</div>}
                    {showDescription === 'maxForce' && <div className="helpText">La fuerza máxima es el límite superior de la fuerza que se puede aplicar al carro.</div>}
                    {showDescription === 'learningRate' && <div className="helpText">La tasa de aprendizaje determina cuánto cambian los parámetros en cada paso de actualización.</div>}
                </div>
            </div>

            {/* Gráficas y botones */}
            <div className="graphsSection">
                <div className="graphsContainer">
                    <h4>Curva de Aprendizaje</h4>
                    <div className="graphBox">Gráfico de episodios vs recompensa</div>
                    <h4>Curva de la política</h4>
                    <div className="graphBox">Gráfico de la política durante el entrenamiento</div>
                    <h4>Tiempo de aprendizaje</h4>
                    <div className="graphBox">Gráfico de tiempo de aprendizaje por política</div>
                </div>
                <div className="actionButtons">
                    <button className="trainButton">Entrenar</button>
                    <button className="simulateButton">Simular</button>
                </div>
            </div>
        </div>
    );
}

export default Cartpole;
