# Teléfono Antiguo

El presente código se utiliza para simular el sonido de un timbre de teléfono antiguo y reproducción de un audio precargado por la bocina del mismo teléfono al levantar el auricular. 

Realizando lo siguiente:

<ol>
  <li>El audio sonará siempre que se levante el auricular y comenzará de cero (V1.0) o se reiniciará del punto donde se quedó (V2.0)</li>
  <li>El audio se repetirá en bucle siempre que esté descolgado el auricular</li>
  <li>Siempre que se cuelgue el auricular se detendrá el audio por completo (V1.0) o se pausará (V2.0)</li>
  <li>El timbre sonará solo si está colgado el auricular y sonará en periodos de entre 20 a 40 minutos dado un número aleatorio.</li>
  <li>El sonido del timbre durará máximo 6 segundos. Sino se levanta el auricular en dicho periodo el timbre se apaga y se genera un nuevo número aleatorio para el periodo de espera entre sonidos del timbre.</li>
</ol>

Se utilizó la librería pygame para el control del audio:
https://www.pygame.org/docs/ref/music.html

<h2>Diagrama de conexiones</h2>


![Diagrama de conexiones](https://github.com/user-attachments/assets/5e895e54-00aa-461b-adfa-26c678601232)
