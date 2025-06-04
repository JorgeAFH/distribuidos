function resetRecursos() {
  const impresora = document.getElementById('impresora');
  const escaner = document.getElementById('escaner');
  const log = document.getElementById('log');

  impresora.className = 'recurso libre';
  impresora.textContent = '🖨️ Impresora (Libre)';
  escaner.className = 'recurso libre';
  escaner.textContent = '📠 Escáner (Libre)';
  log.textContent = '🔁 Estado: Reiniciado.';
}

function bloquear(recurso, proceso) {
  recurso.className = 'recurso ocupado';
  recurso.textContent = recurso.textContent.split(' - ')[0] + ` - Usado por ${proceso}`;
}

function iniciarInterbloqueo() {
  resetRecursos();
  const impresora = document.getElementById('impresora');
  const escaner = document.getElementById('escaner');
  const log = document.getElementById('log');

  log.textContent = '🔄 Iniciando simulación del interbloqueo...';

  setTimeout(() => {
    bloquear(impresora, 'P1');
    log.textContent = '🟦 Proceso 1 ha bloqueado la impresora. Esperará luego por el escáner.';
  }, 1000);

  setTimeout(() => {
    bloquear(escaner, 'P2');
    log.textContent = '🟥 Proceso 2 ha bloqueado el escáner. Esperará luego por la impresora.';
  }, 3000);

  setTimeout(() => {
    log.textContent = '🟦 Proceso 1 ahora intenta usar el escáner, pero está ocupado por el Proceso 2.';
  }, 5000);

  setTimeout(() => {
    log.textContent = '🟥 Proceso 2 ahora intenta usar la impresora, pero está ocupada por el Proceso 1.';
  }, 7000);

  setTimeout(() => {
    log.textContent = '💥 Interbloqueo: Ambos procesos están esperando un recurso que el otro tiene. Ninguno puede continuar.';
  }, 10000);
}
