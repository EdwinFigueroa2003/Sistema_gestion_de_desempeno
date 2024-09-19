Las carpetas que hay aquí, la importante es el "sistemagestiondesempeño" que es el que se actualiza.
La carpeta ENV es un entorno virtual que toca crearlo en cada dispositivo.
El otro archivo en una base de datos que se esta usando de prueba, hasta que se tenga la oficial.


{% extends "layout.html" %}

{% block title %}
Información Proyectos
{% endblock %}

{% block content %}
<h1>Proyectos</h1>
<hr>

<div class="circle-wrapper1">
    <div class="circle1"></div>
</div>


<div class="rectangle-2113"> <!--No lo toco-->
     <titulo-proyecto-principal>Proyecto 1</titulo-proyecto-principal>
    <descripcion-titulo-proyecto-principal>Lorem ipsum dolor se sienta amet, consectetur adipiscing elit. Nullam
        malesuada rutrum diam, sed sollicitudin sed sed.</descripcion-titulo-proyecto-principal>
</div>

<!--Desde aqui se ponen los otros proyectos-->
<!--Estos van juntos-->

<div class="contenedor-proyecto">
    <div class="rectangle-2114">
        <a href="#">
            <titulo-proyecto>Proyecto 1 / Micro Proyecto AAA</titulo-proyecto>
            <p>Lorem ipsum dolor se sienta amet, consectetur adipiscing elit. Nullam malesuada rutrum diam, sed sollicitudin sed sed.</p>
        </a>
    </div>

    <div class="rectangle-2115">
        <descripcion-adicional>Lorem ipsum dolor se sienta amet, consectetur adipiscing elit.<br>
            Nullam malesuada rutrum diam,<br>
            sed sollicitudin sed sed.
        </descripcion-adicional>
        <descargar-informe>Descargar informes</descargar-informe>
    </div>
</div>

<!--Estos van juntos-->
<!--Desde aqui se ponen los otros proyectos-->


<!--Desde aqui se ponen los otros proyectos-->
<!--Estos van juntos-->
<div class="contenedor-proyecto">
    <div class="rectangle-2114">
        <a href="#">
            <titulo-proyecto>Proyecto 1 / Micro Proyecto AAA</titulo-proyecto>
            <p>Lorem ipsum dolor se sienta amet, consectetur adipiscing elit. Nullam malesuada rutrum diam, sed sollicitudin sed sed.</p>
        </a>
    </div>

    <div class="rectangle-2115">
        <descripcion-adicional>Lorem ipsum dolor se sienta amet, consectetur adipiscing elit.<br>
            Nullam malesuada rutrum diam,<br>
            sed sollicitudin sed sed.
        </descripcion-adicional>
        <descargar-informe>Descargar informes</descargar-informe>
    </div>
</div>
<!--Estos van juntos-->
<!--Desde aqui se ponen los otros proyectos-->



<!--Desde aqui se ponen los otros proyectos-->
<!--Estos van juntos-->

<div class="contenedor-proyecto">
    <div class="rectangle-2114">
        <a href="#">
            <titulo-proyecto>Proyecto 1 / Micro Proyecto AAA</titulo-proyecto>
            <p>Lorem ipsum dolor se sienta amet, consectetur adipiscing elit. Nullam malesuada rutrum diam, sed sollicitudin sed sed.</p>
        </a>
    </div>

    <div class="rectangle-2115">
        <descripcion-adicional>Lorem ipsum dolor se sienta amet, consectetur adipiscing elit.<br>
            Nullam malesuada rutrum diam,<br>
            sed sollicitudin sed sed.
        </descripcion-adicional>
        <descargar-informe>Descargar informes</descargar-informe>
    </div>
</div>

<!--Estos van juntos-->
<!--Desde aqui se ponen los otros proyectos-->


<!--Desde aqui se ponen los otros proyectos-->
<!--Estos van juntos-->

<div class="contenedor-proyecto">
    <div class="rectangle-2114">
        <a href="#">
            <titulo-proyecto>Proyecto 1 / Micro Proyecto AAA</titulo-proyecto>
            <p>Lorem ipsum dolor se sienta amet, consectetur adipiscing elit. Nullam malesuada rutrum diam, sed sollicitudin sed sed.</p>
        </a>
    </div>

    <div class="rectangle-2115">
        <descripcion-adicional>Lorem ipsum dolor se sienta amet, consectetur adipiscing elit.<br>
            Nullam malesuada rutrum diam,<br>
            sed sollicitudin sed sed.
        </descripcion-adicional>
        <descargar-informe>Descargar informes</descargar-informe>
    </div>
</div>

<!--Estos van juntos-->
<!--Desde aqui se ponen los otros proyectos-->



<img src="{{ url_for('static', filename='img/mariposa0.png')}}" class="mariposa" />
<img src="{{ url_for('static', filename='img/proyecto-10.png')}}" class="usuarios" />


{% endblock %}

lista de proyectos

{% extends "layout.html" %}

{% block title %}
Proyectos
{% endblock %}

{% block content %}
<h1>Proyectos</h1>
<hr>


{% if proyectos %}
<ul>
    {% for proyecto in proyectos %}
    <a href="/infoproyectos">
    <div class="rectangle-2112">
        <h3>{{ proyecto['nombre_proyecto'] }}</h3>
        <p>{{ proyecto['descripcion_proyecto'] }}</p>
    </div>
    </a>
    {% endfor %}
</ul>
{% else %}
<p>No hay proyectos disponibles.</p>
{% endif %}

<img src="{{ url_for('static', filename='img/mariposa0.png')}}" class="mariposa" />
<img src="{{ url_for('static', filename='img/proyecto-10.png')}}" class="usuarios" />

{% endblock %}