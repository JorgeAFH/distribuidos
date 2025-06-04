package com.team.utils;

import com.team.config.Configuracion;
import com.team.interfaces.Cita;

import javax.swing.*;
import javax.swing.border.*;
import javax.swing.table.*;
import javax.swing.text.StyleConstants;
import java.awt.*;
import java.awt.event.*;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.List;
import java.util.function.BiConsumer;
import java.util.function.Consumer;

/**
 * Clase que implementa la interfaz gráfica del sistema
 */
public class InterfazGrafica {
    // Componentes de la interfaz
    private JFrame ventana;
    private JTabbedPane pestanas;
    private JPanel panelVisualizacion;
    private JPanel panelEstadisticas;
    private JPanel panelRegistro;

    // Componentes para visualización
    private Map<Integer, JTable> tablasSalas = new HashMap<>();
    private Map<Integer, JPanel> panelesDoctores = new HashMap<>();
    private Map<Integer, JLabel> etiquetasDoctores = new HashMap<>();

    // Componentes para estadísticas
    private JLabel lblCitasRegistradas;
    private JLabel lblCitasAtendidas;
    private JLabel lblTiempoEspera;
    private Map<Integer, JLabel> lblTiemposPrioridad = new HashMap<>();
    private JProgressBar barraProgreso;

    // Componentes para registro
    private JTextPane txtRegistro;
    private javax.swing.text.StyledDocument docRegistro;

    // Componentes para control
    private JButton btnIniciar;
    private JButton btnPausar;
    private JSlider sliderVelocidad;
    private JLabel lblVelocidad;

    // Estado de la simulación
    private boolean simulacionIniciada = false;
    private boolean simulacionPausada = false;

    // Datos
    private Map<Integer, List<Cita>> citasEnEspera = new HashMap<>();
    private Map<Integer, Cita> citasEnAtencion = new HashMap<>();
    private Estadisticas estadisticas;
    private Runnable iniciarSimulacionCallback;

    // Formato de fecha
    private SimpleDateFormat formatoHora = new SimpleDateFormat("HH:mm:ss");

    // Colores y fuentes
    private final Color COLOR_FONDO = new Color(245, 245, 250);
    private final Color COLOR_PANEL = new Color(255, 255, 255);
    private final Color COLOR_BORDE = new Color(220, 220, 230);
    private final Color COLOR_TITULO = new Color(70, 90, 120);
    private final Color COLOR_TEXTO = new Color(50, 50, 60);
    private final Color COLOR_TEXTO_SECUNDARIO = new Color(100, 100, 120);

    private final Font FUENTE_TITULO = new Font("Segoe UI", Font.BOLD, 14);
    private final Font FUENTE_SUBTITULO = new Font("Segoe UI", Font.BOLD, 13);
    private final Font FUENTE_NORMAL = new Font("Segoe UI", Font.PLAIN, 12);
    private final Font FUENTE_PEQUEÑA = new Font("Segoe UI", Font.PLAIN, 11);

    // Colores para prioridades
    private final Color[] COLORES_PRIORIDAD = {
            null,
            new Color(220, 53, 69),   // EMERGENCIA - Rojo
            new Color(255, 193, 7),   // URGENTE - Amarillo
            new Color(40, 167, 69),   // PRIORITARIO - Verde
            new Color(0, 123, 255),   // NORMAL - Azul
            new Color(108, 117, 125)  // RUTINA - Gris
    };

    private final String[] NOMBRES_PRIORIDAD = {
            "", "EMERGENCIA", "URGENTE", "PRIORITARIO", "NORMAL", "RUTINA"
    };

    /**
     * Constructor de la interfaz gráfica
     */
    public InterfazGrafica(Estadisticas estadisticas, Runnable iniciarSimulacionCallback) {
        this.estadisticas = estadisticas;
        this.iniciarSimulacionCallback = iniciarSimulacionCallback;

        // Inicializar listas de citas
        for (int i = 1; i <= 5; i++) {
            citasEnEspera.put(i, new ArrayList<>());
        }

        // Registrar callbacks
        Configuracion.registrarCallbackNuevaCita(this::actualizarNuevaCita);
        Configuracion.registrarCallbackAtencionCita(this::actualizarAtencionCita);
        estadisticas.agregarCallback(this::actualizarEstadisticas);

        // Configurar look and feel
        configurarLookAndFeel();

        // Crear la interfaz gráfica
        crearInterfaz();
    }

    /**
     * Configura el look and feel de la aplicación
     */
    private void configurarLookAndFeel() {
        try {
            // Intentar usar el look and feel del sistema
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());

            // Personalizar componentes comunes
            UIManager.put("TabbedPane.selected", new Color(240, 240, 255));
            UIManager.put("TabbedPane.contentAreaColor", COLOR_PANEL);
            UIManager.put("TabbedPane.focus", new Color(220, 220, 240));
            UIManager.put("TabbedPane.light", COLOR_PANEL);
            UIManager.put("TabbedPane.borderHightlightColor", COLOR_BORDE);
            UIManager.put("TabbedPane.contentBorderInsets", new Insets(5, 5, 5, 5));

            UIManager.put("Button.background", new Color(240, 240, 250));
            UIManager.put("Button.select", new Color(220, 220, 240));
            UIManager.put("Button.focus", new Color(220, 220, 240));

            UIManager.put("ProgressBar.selectionBackground", COLOR_TITULO);
            UIManager.put("ProgressBar.selectionForeground", Color.WHITE);

            UIManager.put("Table.gridColor", new Color(240, 240, 245));
            UIManager.put("Table.selectionBackground", new Color(220, 220, 240));
            UIManager.put("Table.selectionForeground", COLOR_TEXTO);

        } catch (Exception e) {
            System.err.println("No se pudo establecer el look and feel: " + e);
        }
    }

    /**
     * Crea la interfaz gráfica
     */
    private void crearInterfaz() {
        // Crear ventana principal
        ventana = new JFrame("Sistema de Gestión de Citas Médicas");
        ventana.setSize(1100, 750);
        ventana.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        ventana.setLayout(new BorderLayout(0, 0));
        ventana.getContentPane().setBackground(COLOR_FONDO);

        // Icono de la aplicación (opcional)
        // ventana.setIconImage(new ImageIcon("ruta/al/icono.png").getImage());

        // Crear pestañas con estilo mejorado
        pestanas = new JTabbedPane();
        pestanas.setFont(FUENTE_SUBTITULO);
        pestanas.setBackground(COLOR_FONDO);
        pestanas.setForeground(COLOR_TEXTO);
        ventana.add(pestanas, BorderLayout.CENTER);

        // Crear paneles para cada pestaña
        panelVisualizacion = new JPanel(new BorderLayout());
        panelVisualizacion.setBackground(COLOR_PANEL);

        panelEstadisticas = new JPanel(new BorderLayout());
        panelEstadisticas.setBackground(COLOR_PANEL);

        panelRegistro = new JPanel(new BorderLayout());
        panelRegistro.setBackground(COLOR_PANEL);

        // Agregar pestañas con iconos
        pestanas.addTab("Visualización", null, panelVisualizacion, "Ver salas de espera y consultas");
        pestanas.addTab("Estadísticas", null, panelEstadisticas, "Ver estadísticas del sistema");
        pestanas.addTab("Registro de Actividad", null, panelRegistro, "Ver registro de eventos");

        // Configurar cada panel
        configurarPanelVisualizacion();
        configurarPanelEstadisticas();
        configurarPanelRegistro();

        // Configurar barra de control
        configurarBarraControl();

        // Mostrar ventana centrada
        ventana.setLocationRelativeTo(null);
        ventana.setVisible(true);
    }

    /**
     * Configura el panel de visualización
     */
    private void configurarPanelVisualizacion() {
        // Panel principal con layout vertical y scroll
        JPanel panelContenido = new JPanel();
        panelContenido.setLayout(new BoxLayout(panelContenido, BoxLayout.Y_AXIS));
        panelContenido.setBackground(COLOR_PANEL);
        panelContenido.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));

        JScrollPane scrollPane = new JScrollPane(panelContenido);
        scrollPane.setBorder(BorderFactory.createEmptyBorder());
        scrollPane.getVerticalScrollBar().setUnitIncrement(16);
        panelVisualizacion.add(scrollPane, BorderLayout.CENTER);

        // Título del panel
        JLabel lblTitulo = new JLabel("Estado Actual del Sistema");
        lblTitulo.setFont(new Font("Segoe UI", Font.BOLD, 18));
        lblTitulo.setForeground(COLOR_TITULO);
        lblTitulo.setAlignmentX(Component.LEFT_ALIGNMENT);
        lblTitulo.setBorder(BorderFactory.createEmptyBorder(0, 0, 15, 0));
        panelContenido.add(lblTitulo);

        // Panel para consultas médicas (arriba)
        JPanel panelConsultas = new JPanel();
        panelConsultas.setLayout(new BoxLayout(panelConsultas, BoxLayout.Y_AXIS));
        panelConsultas.setBackground(COLOR_PANEL);
        panelConsultas.setAlignmentX(Component.LEFT_ALIGNMENT);
        panelConsultas.setBorder(crearBordeTitulado("Consultas Médicas Activas", FUENTE_SUBTITULO));
        panelContenido.add(panelConsultas);

        // Grid para doctores
        JPanel gridDoctores = new JPanel(new GridLayout(0, 3, 10, 10));
        gridDoctores.setBackground(COLOR_PANEL);
        gridDoctores.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        panelConsultas.add(gridDoctores);

        // Crear paneles para cada doctor
        for (int i = 1; i <= Configuracion.NUM_DOCTORES; i++) {
            JPanel panelDoctor = new JPanel(new BorderLayout(5, 5));
            panelDoctor.setBackground(COLOR_PANEL);
            panelDoctor.setBorder(BorderFactory.createCompoundBorder(
                    BorderFactory.createLineBorder(COLOR_BORDE, 1, true),
                    BorderFactory.createEmptyBorder(10, 10, 10, 10)
            ));

            // Cabecera del panel del doctor
            JPanel headerDoctor = new JPanel(new BorderLayout());
            headerDoctor.setBackground(COLOR_PANEL);
            headerDoctor.setBorder(BorderFactory.createEmptyBorder(0, 0, 5, 0));

            JLabel iconoDoctor = new JLabel("\uD83D\uDC68\u200D⚕️"); // Emoji de doctor
            iconoDoctor.setFont(new Font("Segoe UI", Font.PLAIN, 16));
            headerDoctor.add(iconoDoctor, BorderLayout.WEST);

            JLabel etiquetaDoctor = new JLabel("Doctor " + i);
            etiquetaDoctor.setFont(FUENTE_SUBTITULO);
            etiquetaDoctor.setForeground(COLOR_TITULO);
            headerDoctor.add(etiquetaDoctor, BorderLayout.CENTER);

            JLabel estadoDoctor = new JLabel("Disponible");
            estadoDoctor.setFont(FUENTE_PEQUEÑA);
            estadoDoctor.setForeground(new Color(40, 167, 69));
            headerDoctor.add(estadoDoctor, BorderLayout.EAST);

            panelDoctor.add(headerDoctor, BorderLayout.NORTH);

            // Contenido del panel del doctor
            JLabel contenidoDoctor = new JLabel("Sin paciente asignado");
            contenidoDoctor.setFont(FUENTE_NORMAL);
            contenidoDoctor.setForeground(COLOR_TEXTO_SECUNDARIO);
            contenidoDoctor.setBorder(BorderFactory.createEmptyBorder(10, 5, 5, 5));
            panelDoctor.add(contenidoDoctor, BorderLayout.CENTER);

            gridDoctores.add(panelDoctor);
            panelesDoctores.put(i, panelDoctor);
            etiquetasDoctores.put(i, contenidoDoctor);
        }

        // Espacio entre secciones
        panelContenido.add(Box.createRigidArea(new Dimension(0, 20)));

        // Panel para salas de espera
        JPanel panelSalas = new JPanel();
        panelSalas.setLayout(new BoxLayout(panelSalas, BoxLayout.Y_AXIS));
        panelSalas.setBackground(COLOR_PANEL);
        panelSalas.setAlignmentX(Component.LEFT_ALIGNMENT);
        panelSalas.setBorder(crearBordeTitulado("Salas de Espera por Prioridad", FUENTE_SUBTITULO));
        panelContenido.add(panelSalas);

        // Crear tablas para cada sala de espera
        for (int i = 1; i <= 5; i++) {
            JPanel panelNivel = new JPanel(new BorderLayout(10, 0));
            panelNivel.setBackground(COLOR_PANEL);
            panelNivel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
            panelNivel.setAlignmentX(Component.LEFT_ALIGNMENT);

            // Panel de cabecera con color de prioridad
            JPanel headerPrioridad = new JPanel(new BorderLayout());
            headerPrioridad.setBackground(COLORES_PRIORIDAD[i]);
            headerPrioridad.setBorder(BorderFactory.createEmptyBorder(5, 10, 5, 10));

            JLabel etiquetaPrioridad = new JLabel(NOMBRES_PRIORIDAD[i]);
            etiquetaPrioridad.setFont(FUENTE_SUBTITULO);
            etiquetaPrioridad.setForeground(Color.WHITE);
            headerPrioridad.add(etiquetaPrioridad, BorderLayout.WEST);

            JLabel contadorPrioridad = new JLabel("0 pacientes");
            contadorPrioridad.setFont(FUENTE_PEQUEÑA);
            contadorPrioridad.setForeground(Color.WHITE);
            headerPrioridad.add(contadorPrioridad, BorderLayout.EAST);

            panelNivel.add(headerPrioridad, BorderLayout.NORTH);

            // Tabla con estilo mejorado
            DefaultTableModel modelo = new DefaultTableModel(
                    new Object[][] {},
                    new String[] {"ID", "Paciente", "Síntomas", "Tiempo de Espera"}
            ) {
                @Override
                public boolean isCellEditable(int row, int column) {
                    return false;
                }
            };

            JTable tabla = new JTable(modelo);
            tabla.setFont(FUENTE_NORMAL);
            tabla.setRowHeight(25);
            tabla.setIntercellSpacing(new Dimension(5, 5));
            tabla.setShowGrid(false);
            tabla.setFillsViewportHeight(true);

            // Personalizar encabezados
            JTableHeader header = tabla.getTableHeader();
            header.setFont(FUENTE_PEQUEÑA);
            header.setBackground(new Color(245, 245, 250));
            header.setForeground(COLOR_TEXTO);

            // Personalizar columnas
            tabla.getColumnModel().getColumn(0).setPreferredWidth(50);
            tabla.getColumnModel().getColumn(1).setPreferredWidth(150);
            tabla.getColumnModel().getColumn(2).setPreferredWidth(300);
            tabla.getColumnModel().getColumn(3).setPreferredWidth(100);

            // Renderizador personalizado para las celdas
            DefaultTableCellRenderer renderer = new DefaultTableCellRenderer() {
                @Override
                public Component getTableCellRendererComponent(JTable table, Object value, boolean isSelected, boolean hasFocus, int row, int column) {
                    Component c = super.getTableCellRendererComponent(table, value, isSelected, hasFocus, row, column);
                    if (!isSelected) {
                        c.setBackground(row % 2 == 0 ? COLOR_PANEL : new Color(248, 248, 252));
                    }
                    setBorder(BorderFactory.createEmptyBorder(2, 5, 2, 5));
                    return c;
                }
            };

            for (int col = 0; col < tabla.getColumnCount(); col++) {
                tabla.getColumnModel().getColumn(col).setCellRenderer(renderer);
            }

            JScrollPane scrollTabla = new JScrollPane(tabla);
            scrollTabla.setBorder(BorderFactory.createLineBorder(COLOR_BORDE));
            scrollTabla.setBackground(COLOR_PANEL);

            panelNivel.add(scrollTabla, BorderLayout.CENTER);
            panelSalas.add(panelNivel);

            tablasSalas.put(i, tabla);
        }
    }

    /**
     * Configura el panel de estadísticas
     */
    private void configurarPanelEstadisticas() {
        // Panel principal con layout vertical y scroll
        JPanel panelContenido = new JPanel();
        panelContenido.setLayout(new BoxLayout(panelContenido, BoxLayout.Y_AXIS));
        panelContenido.setBackground(COLOR_PANEL);
        panelContenido.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));

        JScrollPane scrollPane = new JScrollPane(panelContenido);
        scrollPane.setBorder(BorderFactory.createEmptyBorder());
        scrollPane.getVerticalScrollBar().setUnitIncrement(16);
        panelEstadisticas.add(scrollPane, BorderLayout.CENTER);

        // Título del panel
        JLabel lblTitulo = new JLabel("Estadísticas del Sistema");
        lblTitulo.setFont(new Font("Segoe UI", Font.BOLD, 18));
        lblTitulo.setForeground(COLOR_TITULO);
        lblTitulo.setAlignmentX(Component.LEFT_ALIGNMENT);
        lblTitulo.setBorder(BorderFactory.createEmptyBorder(0, 0, 15, 0));
        panelContenido.add(lblTitulo);

        // Panel para estadísticas generales
        JPanel panelGeneral = new JPanel();
        panelGeneral.setLayout(new BoxLayout(panelGeneral, BoxLayout.Y_AXIS));
        panelGeneral.setBackground(COLOR_PANEL);
        panelGeneral.setAlignmentX(Component.LEFT_ALIGNMENT);
        panelGeneral.setBorder(crearBordeTitulado("Estadísticas Generales", FUENTE_SUBTITULO));
        panelContenido.add(panelGeneral);

        // Panel de tarjetas para estadísticas principales
        JPanel panelTarjetas = new JPanel(new GridLayout(1, 3, 15, 0));
        panelTarjetas.setBackground(COLOR_PANEL);
        panelTarjetas.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));
        panelTarjetas.setAlignmentX(Component.LEFT_ALIGNMENT);
        panelGeneral.add(panelTarjetas);

        // Tarjeta 1: Citas registradas
        JPanel tarjetaRegistradas = crearTarjetaEstadistica("Citas Registradas", "0", new Color(13, 110, 253), "\uD83D\uDCCB");
        panelTarjetas.add(tarjetaRegistradas);
        lblCitasRegistradas = (JLabel)((JPanel)tarjetaRegistradas.getComponent(1)).getComponent(0);

        // Tarjeta 2: Citas atendidas
        JPanel tarjetaAtendidas = crearTarjetaEstadistica("Citas Atendidas", "0", new Color(25, 135, 84), "\u2705");
        panelTarjetas.add(tarjetaAtendidas);
        lblCitasAtendidas = (JLabel)((JPanel)tarjetaAtendidas.getComponent(1)).getComponent(0);

        // Tarjeta 3: Tiempo promedio
        JPanel tarjetaTiempo = crearTarjetaEstadistica("Tiempo Promedio", "0.00s", new Color(102, 16, 242), "\u23F1");
        panelTarjetas.add(tarjetaTiempo);
        lblTiempoEspera = (JLabel)((JPanel)tarjetaTiempo.getComponent(1)).getComponent(0);

        // Espacio entre secciones
        panelContenido.add(Box.createRigidArea(new Dimension(0, 20)));

        // Panel para tiempos por prioridad
        JPanel panelTiempos = new JPanel();
        panelTiempos.setLayout(new BoxLayout(panelTiempos, BoxLayout.Y_AXIS));
        panelTiempos.setBackground(COLOR_PANEL);
        panelTiempos.setAlignmentX(Component.LEFT_ALIGNMENT);
        panelTiempos.setBorder(crearBordeTitulado("Tiempos de Espera por Prioridad", FUENTE_SUBTITULO));
        panelContenido.add(panelTiempos);

        // Panel de barras para tiempos por prioridad
        JPanel panelBarras = new JPanel(new GridLayout(5, 1, 0, 10));
        panelBarras.setBackground(COLOR_PANEL);
        panelBarras.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));
        panelBarras.setAlignmentX(Component.LEFT_ALIGNMENT);
        panelTiempos.add(panelBarras);

        // Crear barras para cada prioridad
        for (int i = 1; i <= 5; i++) {
            JPanel panelBarra = new JPanel(new BorderLayout(10, 0));
            panelBarra.setBackground(COLOR_PANEL);

            JLabel etiqueta = new JLabel(NOMBRES_PRIORIDAD[i]);
            etiqueta.setFont(FUENTE_NORMAL);
            etiqueta.setForeground(COLOR_TEXTO);
            etiqueta.setPreferredSize(new Dimension(120, 25));
            panelBarra.add(etiqueta, BorderLayout.WEST);

            JProgressBar barra = new JProgressBar(0, 100);
            barra.setValue(0);
            barra.setStringPainted(false);
            barra.setBackground(new Color(240, 240, 245));
            barra.setForeground(COLORES_PRIORIDAD[i]);
            panelBarra.add(barra, BorderLayout.CENTER);

            JLabel valor = new JLabel("0.00s");
            valor.setFont(FUENTE_NORMAL);
            valor.setForeground(COLOR_TEXTO);
            valor.setPreferredSize(new Dimension(80, 25));
            valor.setHorizontalAlignment(SwingConstants.RIGHT);
            panelBarra.add(valor, BorderLayout.EAST);

            panelBarras.add(panelBarra);
            lblTiemposPrioridad.put(i, valor);
        }

        // Espacio entre secciones
        panelContenido.add(Box.createRigidArea(new Dimension(0, 20)));

        // Panel para barra de progreso
        JPanel panelProgreso = new JPanel(new BorderLayout());
        panelProgreso.setBackground(COLOR_PANEL);
        panelProgreso.setAlignmentX(Component.LEFT_ALIGNMENT);
        panelProgreso.setBorder(crearBordeTitulado("Progreso de la Simulación", FUENTE_SUBTITULO));
        panelContenido.add(panelProgreso);

        JPanel contenidoProgreso = new JPanel(new BorderLayout(0, 10));
        contenidoProgreso.setBackground(COLOR_PANEL);
        contenidoProgreso.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));
        panelProgreso.add(contenidoProgreso, BorderLayout.CENTER);

        JLabel lblProgreso = new JLabel("Progreso total de citas atendidas:");
        lblProgreso.setFont(FUENTE_NORMAL);
        lblProgreso.setForeground(COLOR_TEXTO);
        contenidoProgreso.add(lblProgreso, BorderLayout.NORTH);

        barraProgreso = new JProgressBar(0, 100);
        barraProgreso.setValue(0);
        barraProgreso.setStringPainted(true);
        barraProgreso.setFont(FUENTE_NORMAL);
        barraProgreso.setBackground(new Color(240, 240, 245));
        barraProgreso.setForeground(new Color(13, 110, 253));
        barraProgreso.setBorder(BorderFactory.createEmptyBorder());
        barraProgreso.setPreferredSize(new Dimension(0, 25));
        contenidoProgreso.add(barraProgreso, BorderLayout.CENTER);
    }

    /**
     * Crea una tarjeta para mostrar una estadística
     */
    private JPanel crearTarjetaEstadistica(String titulo, String valor, Color color, String icono) {
        JPanel tarjeta = new JPanel(new BorderLayout());
        tarjeta.setBackground(COLOR_PANEL);
        tarjeta.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(230, 230, 240), 1, true),
                BorderFactory.createEmptyBorder(15, 15, 15, 15)
        ));

        // Cabecera con título e icono
        JPanel header = new JPanel(new BorderLayout());
        header.setBackground(COLOR_PANEL);
        header.setBorder(BorderFactory.createEmptyBorder(0, 0, 10, 0));

        JLabel lblTitulo = new JLabel(titulo);
        lblTitulo.setFont(FUENTE_PEQUEÑA);
        lblTitulo.setForeground(COLOR_TEXTO_SECUNDARIO);
        header.add(lblTitulo, BorderLayout.WEST);

        JLabel lblIcono = new JLabel(icono);
        lblIcono.setFont(new Font("Segoe UI", Font.PLAIN, 16));
        lblIcono.setForeground(color);
        header.add(lblIcono, BorderLayout.EAST);

        tarjeta.add(header, BorderLayout.NORTH);

        // Valor principal
        JPanel contenido = new JPanel(new BorderLayout());
        contenido.setBackground(COLOR_PANEL);

        JLabel lblValor = new JLabel(valor);
        lblValor.setFont(new Font("Segoe UI", Font.BOLD, 24));
        lblValor.setForeground(color);
        contenido.add(lblValor, BorderLayout.CENTER);

        tarjeta.add(contenido, BorderLayout.CENTER);

        return tarjeta;
    }

    /**
     * Configura el panel de registro de actividad
     */
    private void configurarPanelRegistro() {
        // Panel principal con layout vertical y scroll
        JPanel panelContenido = new JPanel(new BorderLayout());
        panelContenido.setBackground(COLOR_PANEL);
        panelContenido.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));
        panelRegistro.add(panelContenido, BorderLayout.CENTER);

        // Título del panel
        JLabel lblTitulo = new JLabel("Registro de Actividad del Sistema");
        lblTitulo.setFont(new Font("Segoe UI", Font.BOLD, 18));
        lblTitulo.setForeground(COLOR_TITULO);
        panelContenido.add(lblTitulo, BorderLayout.NORTH);

        // Crear área de texto con estilos
        txtRegistro = new JTextPane();
        txtRegistro.setEditable(false);
        txtRegistro.setFont(new Font("Consolas", Font.PLAIN, 13));
        txtRegistro.setBackground(new Color(250, 250, 255));

        // Documento con estilos
        docRegistro = txtRegistro.getStyledDocument();

        // Definir estilos
        javax.swing.text.Style estiloBase = txtRegistro.addStyle("base", null);
        StyleConstants.setFontFamily(estiloBase, "Consolas");
        StyleConstants.setFontSize(estiloBase, 13);

        javax.swing.text.Style estiloInfo = txtRegistro.addStyle("info", estiloBase);
        StyleConstants.setForeground(estiloInfo, COLOR_TEXTO);

        javax.swing.text.Style estiloRecepcion = txtRegistro.addStyle("recepcion", estiloBase);
        StyleConstants.setForeground(estiloRecepcion, new Color(13, 110, 253));

        javax.swing.text.Style estiloAtencion = txtRegistro.addStyle("atencion", estiloBase);
        StyleConstants.setForeground(estiloAtencion, new Color(25, 135, 84));

        javax.swing.text.Style estiloEmergencia = txtRegistro.addStyle("emergencia", estiloBase);
        StyleConstants.setForeground(estiloEmergencia, new Color(220, 53, 69));

        // Scroll para el área de texto
        JScrollPane scrollRegistro = new JScrollPane(txtRegistro);
        scrollRegistro.setBorder(BorderFactory.createLineBorder(COLOR_BORDE));
        scrollRegistro.setBackground(COLOR_PANEL);
        scrollRegistro.setBorder(BorderFactory.createEmptyBorder(15, 0, 0, 0));
        panelContenido.add(scrollRegistro, BorderLayout.CENTER);

        // Mensaje inicial
        agregarRegistro("Sistema de Gestión de Citas Médicas iniciado", "info");
    }

    /**
     * Configura la barra de control
     */
    private void configurarBarraControl() {
        JPanel panelControl = new JPanel();
        panelControl.setLayout(new FlowLayout(FlowLayout.CENTER, 15, 10));
        panelControl.setBackground(new Color(240, 240, 250));
        panelControl.setBorder(BorderFactory.createMatteBorder(1, 0, 0, 0, COLOR_BORDE));
        ventana.add(panelControl, BorderLayout.SOUTH);

        // Botón para iniciar/detener simulación
        btnIniciar = new JButton("Iniciar Simulación");
        btnIniciar.setFont(FUENTE_NORMAL);
        btnIniciar.setForeground(Color.WHITE);
        btnIniciar.setBackground(new Color(13, 110, 253));
        btnIniciar.setFocusPainted(false);
        btnIniciar.setBorder(BorderFactory.createEmptyBorder(8, 15, 8, 15));
        btnIniciar.setCursor(new Cursor(Cursor.HAND_CURSOR));
        btnIniciar.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                toggleSimulacion();
            }
        });
        panelControl.add(btnIniciar);

        // Botón para pausar/reanudar simulación
        btnPausar = new JButton("Pausar");
        btnPausar.setFont(FUENTE_NORMAL);
        btnPausar.setForeground(COLOR_TEXTO);
        btnPausar.setBackground(new Color(240, 240, 240));
        btnPausar.setFocusPainted(false);
        btnPausar.setBorder(BorderFactory.createEmptyBorder(8, 15, 8, 15));
        btnPausar.setCursor(new Cursor(Cursor.HAND_CURSOR));
        btnPausar.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                togglePausa();
            }
        });
        btnPausar.setEnabled(false);
        panelControl.add(btnPausar);

        // Separador vertical
        JSeparator separador = new JSeparator(JSeparator.VERTICAL);
        separador.setPreferredSize(new Dimension(1, 30));
        separador.setForeground(COLOR_BORDE);
        panelControl.add(separador);

    }

    /**
     * Crea un borde con título para los paneles
     */
    private Border crearBordeTitulado(String titulo, Font fuente) {
        TitledBorder borde = BorderFactory.createTitledBorder(
                BorderFactory.createLineBorder(COLOR_BORDE, 1, true),
                titulo
        );
        borde.setTitleFont(fuente);
        borde.setTitleColor(COLOR_TITULO);
        borde.setTitlePosition(TitledBorder.ABOVE_TOP);
        borde.setTitleJustification(TitledBorder.LEFT);

        return BorderFactory.createCompoundBorder(
                borde,
                BorderFactory.createEmptyBorder(5, 5, 5, 5)
        );
    }

    /**
     * Inicia o detiene la simulación
     */
    private void toggleSimulacion() {
        if (!simulacionIniciada) {
            // Iniciar simulación
            simulacionIniciada = true;
            btnIniciar.setText("Detener Simulación");
            btnIniciar.setBackground(new Color(220, 53, 69));
            btnPausar.setEnabled(true);

            // Llamar al callback para iniciar la simulación
            new Thread(iniciarSimulacionCallback).start();

            agregarRegistro("Simulación iniciada", "info");
        } else {
            // Preguntar si realmente quiere detener
            int respuesta = JOptionPane.showConfirmDialog(
                    ventana,
                    "¿Está seguro de que desea detener la simulación?",
                    "Detener Simulación",
                    JOptionPane.YES_NO_OPTION,
                    JOptionPane.QUESTION_MESSAGE
            );

            if (respuesta == JOptionPane.YES_OPTION) {
                // Detener simulación (cerrar la aplicación)
                System.exit(0);
            }
        }
    }

    /**
     * Pausa o reanuda la simulación
     */
    private void togglePausa() {
        if (!simulacionPausada) {
            // Pausar simulación
            simulacionPausada = true;
            btnPausar.setText("Reanudar");
            btnPausar.setBackground(new Color(255, 193, 7));
            btnPausar.setForeground(COLOR_TEXTO);
            Configuracion.pausarSimulacion();
            agregarRegistro("Simulación pausada", "info");
        } else {
            // Reanudar simulación
            simulacionPausada = false;
            btnPausar.setText("Pausar");
            btnPausar.setBackground(new Color(240, 240, 240));
            btnPausar.setForeground(COLOR_TEXTO);
            Configuracion.reanudarSimulacion();
            agregarRegistro("Simulación reanudada", "info");
        }
    }

    /**
     * Cambia la velocidad de la simulación
     */
    private void cambiarVelocidad() {
        double valor = sliderVelocidad.getValue() / 10.0;
        lblVelocidad.setText(String.format("%.1fx", valor));
        Configuracion.establecerVelocidad(1.0 / valor);  // Invertimos el valor para que mayor = más rápido
    }

    /**
     * Callback que se llama cuando se registra una nueva cita
     */
    public void actualizarNuevaCita(Cita cita) {
        // Agregar cita a la lista de espera correspondiente
        citasEnEspera.get(cita.getPrioridad()).add(cita);

        // Actualizar la interfaz (en el hilo de la interfaz gráfica)
        SwingUtilities.invokeLater(this::actualizarInterfaz);

        // Agregar al registro
        String nivelPrioridad = cita.obtenerNivelPrioridad();
        String mensaje = "Nueva cita registrada: " + cita.getPaciente() + " - " + nivelPrioridad + " - " + cita.getSintomas();
        String tipo = "recepcion";
        if (cita.getPrioridad() == 1) {  // Emergencia
            tipo = "emergencia";
        }
        agregarRegistro(mensaje, tipo);
    }

    /**
     * Callback que se llama cuando un doctor atiende una cita
     */
    public void actualizarAtencionCita(Cita cita, Integer doctorId) {
        // Quitar cita de la lista de espera
        citasEnEspera.get(cita.getPrioridad()).remove(cita);

        // Agregar cita a la lista de atención
        citasEnAtencion.put(doctorId, cita);

        // Actualizar la interfaz (en el hilo de la interfaz gráfica)
        SwingUtilities.invokeLater(this::actualizarInterfaz);

        // Agregar al registro
        String nivelPrioridad = cita.obtenerNivelPrioridad();
        String mensaje = "Doctor " + doctorId + " atiende a " + cita.getPaciente() + " - " + nivelPrioridad;
        agregarRegistro(mensaje, "atencion");
    }

    /**
     * Callback que se llama cuando cambian las estadísticas
     */
    public void actualizarEstadisticas(Map<String, Object> informe) {
        // Actualizar la interfaz (en el hilo de la interfaz gráfica)
        SwingUtilities.invokeLater(() -> actualizarPanelEstadisticas(informe));
    }

    /**
     * Actualiza todos los elementos de la interfaz gráfica
     */
    private void actualizarInterfaz() {
        // Actualizar tablas de salas de espera
        for (int prioridad = 1; prioridad <= 5; prioridad++) {
            DefaultTableModel modelo = (DefaultTableModel) tablasSalas.get(prioridad).getModel();
            modelo.setRowCount(0);  // Limpiar tabla

            // Agregar citas en espera
            List<Cita> citas = citasEnEspera.get(prioridad);
            for (Cita cita : citas) {
                long tiempoEspera = (System.currentTimeMillis() - cita.getTiempoRegistro()) / 1000;
                modelo.addRow(new Object[] {
                        cita.getId(),
                        cita.getPaciente(),
                        cita.getSintomas(),
                        String.format("%d:%02d", tiempoEspera / 60, tiempoEspera % 60)
                });
            }

            // Actualizar contador en la cabecera
            JTable tabla = tablasSalas.get(prioridad);
            Container parent = tabla.getParent().getParent();
            if (parent instanceof JPanel) {
                JPanel panelNivel = (JPanel) parent;
                JPanel headerPrioridad = (JPanel) panelNivel.getComponent(0);
                JLabel contadorPrioridad = (JLabel) headerPrioridad.getComponent(1);
                contadorPrioridad.setText(citas.size() + " pacientes");
            }
        }

        // Actualizar paneles de doctores
        for (int doctorId = 1; doctorId <= Configuracion.NUM_DOCTORES; doctorId++) {
            JPanel panelDoctor = panelesDoctores.get(doctorId);
            JLabel contenidoDoctor = etiquetasDoctores.get(doctorId);

            if (citasEnAtencion.containsKey(doctorId)) {
                Cita cita = citasEnAtencion.get(doctorId);

                // Actualizar contenido
                String texto = "<html><b>Paciente:</b> " + cita.getPaciente() +
                        "<br><b>Prioridad:</b> " + cita.obtenerNivelPrioridad() +
                        "<br><b>Síntomas:</b> " + cita.getSintomas() + "</html>";
                contenidoDoctor.setText(texto);

                // Actualizar estado del doctor
                JPanel headerDoctor = (JPanel) panelDoctor.getComponent(0);
                JLabel estadoDoctor = (JLabel) headerDoctor.getComponent(2);
                estadoDoctor.setText("Ocupado");
                estadoDoctor.setForeground(new Color(220, 53, 69));

                // Actualizar color de fondo según prioridad
                panelDoctor.setBackground(new Color(255, 255, 255));
                panelDoctor.setBorder(BorderFactory.createCompoundBorder(
                        BorderFactory.createLineBorder(COLORES_PRIORIDAD[cita.getPrioridad()], 2, true),
                        BorderFactory.createEmptyBorder(10, 10, 10, 10)
                ));
            } else {
                // Restablecer panel
                contenidoDoctor.setText("Sin paciente asignado");

                // Actualizar estado del doctor
                JPanel headerDoctor = (JPanel) panelDoctor.getComponent(0);
                JLabel estadoDoctor = (JLabel) headerDoctor.getComponent(2);
                estadoDoctor.setText("Disponible");
                estadoDoctor.setForeground(new Color(40, 167, 69));

                // Restablecer color de fondo
                panelDoctor.setBackground(COLOR_PANEL);
                panelDoctor.setBorder(BorderFactory.createCompoundBorder(
                        BorderFactory.createLineBorder(COLOR_BORDE, 1, true),
                        BorderFactory.createEmptyBorder(10, 10, 10, 10)
                ));
            }
        }
    }

    /**
     * Actualiza los elementos del panel de estadísticas
     */
    private void actualizarPanelEstadisticas(Map<String, Object> informe) {
        // Actualizar etiquetas de estadísticas generales
        lblCitasRegistradas.setText(informe.get("citasRegistradas").toString());
        lblCitasAtendidas.setText(informe.get("citasAtendidas").toString());
        lblTiempoEspera.setText(String.format("%.2fs", (Double) informe.get("tiempoEsperaPromedio")));

        // Actualizar etiquetas de tiempos por prioridad
        Map<Integer, Double> tiemposPorPrioridad = (Map<Integer, Double>) informe.get("tiemposPorPrioridad");
        for (int prioridad = 1; prioridad <= 5; prioridad++) {
            double tiempo = tiemposPorPrioridad.get(prioridad);
            lblTiemposPrioridad.get(prioridad).setText(String.format("%.2fs", tiempo));

            // Actualizar barra de progreso
            JLabel label = lblTiemposPrioridad.get(prioridad);
            Container parent = label.getParent();
            if (parent instanceof JPanel) {
                JPanel panelBarra = (JPanel) parent;
                JProgressBar barra = (JProgressBar) panelBarra.getComponent(1);

                // Calcular valor para la barra (máximo 100)
                int valor = (int) Math.min(100, tiempo / 2);
                barra.setValue(valor);
            }
        }

        // Actualizar barra de progreso
        int totalCitas = Configuracion.NUM_RECEPCIONISTAS * Configuracion.NUM_CITAS_POR_RECEPCIONISTA;
        int citasAtendidas = (Integer) informe.get("citasAtendidas");
        int progreso = (citasAtendidas * 100) / totalCitas;
        barraProgreso.setValue(progreso);
        barraProgreso.setString(citasAtendidas + " de " + totalCitas + " citas (" + progreso + "%)");
    }

    /**
     * Agrega un mensaje al registro de actividad
     */
    public void agregarRegistro(String mensaje, String tipo) {
        String hora = formatoHora.format(new Date());
        String textoFormateado = "[" + hora + "] " + mensaje + "\n";

        try {
            // Agregar texto con estilo
            docRegistro.insertString(docRegistro.getLength(), textoFormateado, txtRegistro.getStyle(tipo));

            // Desplazar al final
            txtRegistro.setCaretPosition(docRegistro.getLength());
        } catch (Exception e) {
            System.err.println("Error al agregar texto al registro: " + e);
        }
    }

    /**
     * Inicia la interfaz gráfica
     */

}
