function iniciarSolucion() {
  resetRecursos();
  const impresora = document.getElementById('impresora');
  const escaner = document.getElementById('escaner');
  const log = document.getElementById('log');

  log.textContent = '🔄 Iniciando simulación de solución al interbloqueo...';

  setTimeout(() => {
    bloquear(impresora, 'P1');
    log.textContent = '🟦 Proceso 1 ha solicitado la impresora y la ha bloqueado.';
  }, 1000);

  setTimeout(() => {
    bloquear(escaner, 'P1');
    log.textContent = '🟦 Proceso 1 ahora solicita el escáner. Como está libre, también lo bloquea.';
  }, 3000);

  setTimeout(() => {
    log.textContent = '🟦 Proceso 1 ya tiene impresora y escáner. Está trabajando con ambos recursos.';
  }, 5000);

  setTimeout(() => {
    impresora.className = 'recurso libre';
    escaner.className = 'recurso libre';
    impresora.textContent = '🖨️ Impresora (Libre)';
    escaner.textContent = '📠 Escáner (Libre)';
    log.textContent = '✅ Proceso 1 terminó su tarea y liberó ambos recursos.';
  }, 8000);

  setTimeout(() => {
    bloquear(impresora, 'P2');
    log.textContent = '🟥 Proceso 2 ahora solicita la impresora. Está libre, así que la bloquea.';
  }, 10000);

  setTimeout(() => {
    bloquear(escaner, 'P2');
    log.textContent = '🟥 Proceso 2 solicita el escáner y también lo bloquea.';
  }, 12000);

  setTimeout(() => {
    log.textContent = '🟥 Proceso 2 ya tiene ambos recursos y está ejecutando su tarea.';
  }, 14000);

  setTimeout(() => {
    impresora.className = 'recurso libre';
    escaner.className = 'recurso libre';
    impresora.textContent = '🖨️ Impresora (Libre)';
    escaner.textContent = '📠 Escáner (Libre)';
    log.textContent = '🎉 Ambos procesos trabajaron correctamente sin interbloqueo.';
  }, 17000);
}
