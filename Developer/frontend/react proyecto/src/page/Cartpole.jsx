import './Cartpole.css';
import { useState } from 'react';

function Cartpole() {
    const [showDescription, setShowDescription] = useState(null);
    const [isActive, setisActive] = useState(true);

    const toggleDescription = (param) => {
        setShowDescription(showDescription === param ? null : param);
    };

    return (
        <div className="contentMain">
            {/* Navbar */}
            <div className="navbar">
                <span className="navbarTitle">Cart Pole</span>
                {/* <span className="navbarItem">Nosotros</span> */}
            </div>

            {/* Parametros */}
            <div className="contentParameter">
                {/* <div className="parameterBox"> */}
                    <label className='variables'>
                        <div>Epsilon</div>
                        <input type="number" name="epsilon" disabled={!isActive}/>
                        <button onClick={() => toggleDescription('epsilon')} className="helpButton">?</button>
                    </label>
                    <label className='variables'>
                        <div>Epsilon decay</div>
                        <input type="number" name="epsilonDecay" disabled={!isActive}/>
                        <button onClick={() => toggleDescription('epsilonDecay')} className="helpButton">?</button>
                    </label>

                    <label className='variables'>
                        <div>Epsilon minimo</div>
                        <input type="number" name="epsilonMinimum" disabled={!isActive}/>
                        <button onClick={() => toggleDescription('epsilonMinimum')} className="helpButton">?</button>
                    </label>

                    <label className='variables'>
                        <div>Gamma</div>
                        <input type="number" name="gamma" disabled={!isActive}/>
                        <button onClick={() => toggleDescription('gamma')} className="helpButton">?</button>
                    </label>

                    <label className='variables'>
                        <div>Masa de Carro</div>
                        <input type="number" name="massCar" disabled={!isActive}/>
                        <button onClick={() => toggleDescription('massCar')} className="helpButton">?</button>
                    </label>

                    <label className='variables'>
                        <div>Masa del Pendulo</div>
                        <input type="number" name="massPendulum" disabled={!isActive}/>
                        <button onClick={() => toggleDescription('massPendulum')} className="helpButton">?</button>
                    </label>

                    <label className='variables'>
                        <div>Longitud del Péndulo</div>
                        <input type="number" name="pendulumLength" disabled={!isActive}/>
                        <button onClick={() => toggleDescription('pendulumLength')} className="helpButton">?</button>
                    </label>

                    <label className='variables'>
                        <div>Fuerza Máxima</div>
                        <input type="number" name="maxForce" disabled={!isActive}/>
                        <button onClick={() => toggleDescription('maxForce')} className="helpButton">?</button>
                    </label>

                    <label className='variables'>
                        <div>N° Episodios</div>
                        <input type="number" name="nepisodes" disabled={!isActive}/>
                        <button onClick={() => toggleDescription('numEpisodes')} className="helpButton">?</button>
                    </label>

                    <label className='variables'>
                        <div>N° Acciones</div>
                        <input type="number" name="nactions" disabled={!isActive}/>
                        <button onClick={() => toggleDescription('numAction')} className="helpButton">?</button>
                    </label>

                    <label className='variables'>
                        <div>N° Estados</div>
                        <input type="number" name="nstates" disabled={!isActive}/>
                        <button onClick={() => toggleDescription('numState')} className="helpButton">?</button>
                    </label>

                    <label className='variables'>
                        <div>Tasa de Aprendizaje</div>
                        <input type="number" name="learningRate" disabled={!isActive}/>
                        <button onClick={() => toggleDescription('learningRate')} className="helpButton">?</button>
                    </label>

                    <label className='variables'>
                        <div>Gravedad</div>
                        <input type="number" name="gravity" disabled={!isActive}/>
                        <button onClick={() => toggleDescription('gravity')} className="helpButton">?</button>
                    </label>
                    <div className='containerButton'><button className="parameterButton" onClick={()=>setisActive(true)}
                    >Editar</button></div>
                    <div className='containerButton'><button className="parameterButton" onClick={()=>setisActive(false)}>Confirmar</button></div>

                    <label className='variables'>
                        <div>Damping</div>
                        <input type="number" name="damping" disabled={!isActive}/>
                        <button onClick={() => toggleDescription('damping')} className="helpButton">?</button>
                    </label>

                {/* </div> */}
            </div>

            {/* Simulador */}
            <div className="contentSimulator">
                <div className="carruselSimulator">
                    <div className="carouselItem">Simulación 1</div>
                    <div className="carouselItem">Simulación 2</div>
                    <button className="nextButton">Siguiente</button>
                </div>
                <div className="leyenda">
                    <h2>Descripción de los parámetros</h2>
                    <p>Haz clic en el signo de interrogación junto a los parámetros para más detalles.</p>
                    {showDescription === 'epsilon' && <div className="helpText">Epsilon controla la exploración del agente. Un valor alto significa más exploración.</div>}
                    {showDescription === 'gamma' && <div className="helpText">Gamma es el factor de descuento para el valor futuro de las recompensas.</div>}
                    {showDescription === 'massCar' && <div className="helpText">La masa del carro es un parámetro importante que influye en la dinámica del sistema.</div>}
                    {showDescription === 'pendulumLength' && <div className="helpText">La longitud del péndulo influye en la estabilidad y el comportamiento del sistema.</div>}
                    {showDescription === 'maxForce' && <div className="helpText">La fuerza máxima es el límite superior de la fuerza que se puede aplicar al carro.</div>}
                    {showDescription === 'learningRate' && <div className="helpText">La tasa de aprendizaje determina cuánto cambian los parámetros en cada paso de actualización.</div>}
                    {showDescription === 'massPendulum' && <div className="helpText">Indica la masa del péndulo, que afecta la dinámica del sistema y su interacción con el carro, también expresada en kilogramos.</div>}
                    {showDescription === 'gravity' && <div className="helpText"> Es la aceleración debida a la gravedad, generalmente fijada en 9.81 m/s², que actúa sobre el péndulo y afecta su movimiento.</div>}
                    {showDescription === 'damping' && <div className="helpText">Se refiere al coeficiente de amortiguamiento, que representa la resistencia al movimiento y ayuda a modelar la pérdida de energía en el sistema.</div>}
                    {showDescription === 'epsilonDecay' && <div className="helpText">Es la tasa a la que el valor de epsilon disminuye, controlando cómo se reduce la exploración a medida que el agente gana experiencia.</div>}
                    {showDescription === 'epsilonMinimum' && <div className="helpText">Es el valor mínimo que epsilon puede alcanzar, asegurando que siempre haya un nivel de exploración incluso en etapas avanzadas del entrenamiento.</div>}
                    {showDescription === 'numEpisodes' && <div className="helpText">Representa el número total de episodios de entrenamiento que el agente ejecutará para aprender a controlar el sistema.</div>}
                    {showDescription === 'numAction' && <div className="helpText">Indica el número de acciones posibles que el agente puede tomar en cualquier estado, influenciando su capacidad para interactuar con el entorno.</div>}
                    {showDescription === 'numState' && <div className="helpText">Es el número de estados discretos en los que se puede dividir el espacio de estado del entorno, facilitando la representación y el aprendizaje.</div>}
                </div>
            </div>

            {/* Gráficas y botones */}
            <div className="actionButtons">
                    <button className="trainButton">Entrenar</button>
                    <button className="simulateButton">Simular</button>
            </div>
            <div className="graphsSection">
                <div className="graphsContainer">
                    <h3>Curva de Aprendizaje</h3>
                    <div className='container-graph'>
                    <div className="graphBox"><p>Gráfico de episodios vs recompensa</p></div>
                    <div className='detalles-graphbox'></div>
                    </div>
                    <h3>Curva de la política</h3>
                    <div className='container-graph'>
                    <div className="graphBox"><p>Gráfico de la política durante el entrenamiento</p></div>
                    <div className='detalles-graphbox'></div>
                    </div>
                    <h3>Tiempo de aprendizaje</h3>
                    <div className='container-graph'>
                    <div className="graphBox"><p>Gráfico de tiempo de aprendizaje por política</p></div>
                    <div className='detalles-graphbox'></div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Cartpole;
