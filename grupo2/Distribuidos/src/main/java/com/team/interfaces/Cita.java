package com.team.interfaces;


public class Cita {
    private final int id;
    private final int prioridad;           // Nivel de urgencia (1=emergencia, 5=rutina)
    private final String paciente;         // Nombre del paciente
    private final String sintomas;         // Descripción de los síntomas
    private final long tiempoRegistro;     // Momento en que se registró la cita

    public Cita(int id, int prioridad, String paciente, String sintomas, long tiempoRegistro) {
        this.id = id;
        this.prioridad = prioridad;
        this.paciente = paciente;
        this.sintomas = sintomas;
        this.tiempoRegistro = tiempoRegistro;
    }

    public int getId() {
        return id;
    }

    public int getPrioridad() {
        return prioridad;
    }

    public String getPaciente() {
        return paciente;
    }

    public String getSintomas() {
        return sintomas;
    }

    public long getTiempoRegistro() {
        return tiempoRegistro;
    }

    public String obtenerNivelPrioridad() {
        String[] niveles = {"", "EMERGENCIA", "URGENTE", "PRIORITARIO", "NORMAL", "RUTINA"};
        return niveles[prioridad];
    }

    public String obtenerColorPrioridad() {
        String[] colores = {"", "#ff0000", "#ff6600", "#ffcc00", "#66cc00", "#00cc66"};
        return colores[prioridad];
    }

    @Override
    public String toString() {
        return "Cita[ID=" + id + ", Paciente='" + paciente + "', Prioridad=" + obtenerNivelPrioridad() + "]";
    }
}
