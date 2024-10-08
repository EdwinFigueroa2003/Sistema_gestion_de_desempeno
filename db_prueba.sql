PGDMP     "                    |         	   db_prueba    15.2    15.2     #           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            $           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            %           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            &           1262    18990 	   db_prueba    DATABASE        CREATE DATABASE db_prueba WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Colombia.1252';
    DROP DATABASE db_prueba;
                postgres    false            �            1259    19014    costo    TABLE     �   CREATE TABLE public.costo (
    id_costo integer NOT NULL,
    nombre_costo character varying(200),
    estado_costo character varying(20)
);
    DROP TABLE public.costo;
       public         heap    postgres    false            �            1259    19019    costo_id_costo_seq    SEQUENCE     �   ALTER TABLE public.costo ALTER COLUMN id_costo ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.costo_id_costo_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    217            �            1259    19020 	   dimension    TABLE     \  CREATE TABLE public.dimension (
    id_dimen integer NOT NULL,
    nombre_dimen character varying(80),
    descripcion_dimen character varying(900),
    incripcion_verde_dimen character varying(400),
    inscripcion_amarillo_dimen character varying(400),
    inscripcion_rojo_dimen character varying(400),
    estado_dimen character varying(20)
);
    DROP TABLE public.dimension;
       public         heap    postgres    false            �            1259    19007 	   estamento    TABLE     l   CREATE TABLE public.estamento (
    id_estam integer[] NOT NULL,
    nombre_estam character varying(500)
);
    DROP TABLE public.estamento;
       public         heap    postgres    false            �            1259    19027    nivel_contrib    TABLE     k   CREATE TABLE public.nivel_contrib (
    id_nivel integer NOT NULL,
    tipo_nivel character varying(50)
);
 !   DROP TABLE public.nivel_contrib;
       public         heap    postgres    false            �            1259    18998    rol    TABLE     [   CREATE TABLE public.rol (
    nombre_rol character varying,
    id_rol integer NOT NULL
);
    DROP TABLE public.rol;
       public         heap    postgres    false            �            1259    19032 	   tipo_eval    TABLE     j   CREATE TABLE public.tipo_eval (
    id_tipo_eval integer NOT NULL,
    tipo_eval character varying(80)
);
    DROP TABLE public.tipo_eval;
       public         heap    postgres    false            �            1259    18991    usuario    TABLE     r   CREATE TABLE public.usuario (
    email character varying(500) NOT NULL,
    contrasena character varying(500)
);
    DROP TABLE public.usuario;
       public         heap    postgres    false                      0    19014    costo 
   TABLE DATA           E   COPY public.costo (id_costo, nombre_costo, estado_costo) FROM stdin;
    public          postgres    false    217   :                 0    19020 	   dimension 
   TABLE DATA           �   COPY public.dimension (id_dimen, nombre_dimen, descripcion_dimen, incripcion_verde_dimen, inscripcion_amarillo_dimen, inscripcion_rojo_dimen, estado_dimen) FROM stdin;
    public          postgres    false    219   W                 0    19007 	   estamento 
   TABLE DATA           ;   COPY public.estamento (id_estam, nombre_estam) FROM stdin;
    public          postgres    false    216   t                 0    19027    nivel_contrib 
   TABLE DATA           =   COPY public.nivel_contrib (id_nivel, tipo_nivel) FROM stdin;
    public          postgres    false    220   �                 0    18998    rol 
   TABLE DATA           1   COPY public.rol (nombre_rol, id_rol) FROM stdin;
    public          postgres    false    215   �                  0    19032 	   tipo_eval 
   TABLE DATA           <   COPY public.tipo_eval (id_tipo_eval, tipo_eval) FROM stdin;
    public          postgres    false    221   �                 0    18991    usuario 
   TABLE DATA           4   COPY public.usuario (email, contrasena) FROM stdin;
    public          postgres    false    214   �       '           0    0    costo_id_costo_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.costo_id_costo_seq', 1, false);
          public          postgres    false    218            �           2606    19018    costo costo_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.costo
    ADD CONSTRAINT costo_pkey PRIMARY KEY (id_costo);
 :   ALTER TABLE ONLY public.costo DROP CONSTRAINT costo_pkey;
       public            postgres    false    217            �           2606    19026    dimension dimension_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.dimension
    ADD CONSTRAINT dimension_pkey PRIMARY KEY (id_dimen);
 B   ALTER TABLE ONLY public.dimension DROP CONSTRAINT dimension_pkey;
       public            postgres    false    219            �           2606    19013    estamento estamento_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.estamento
    ADD CONSTRAINT estamento_pkey PRIMARY KEY (id_estam);
 B   ALTER TABLE ONLY public.estamento DROP CONSTRAINT estamento_pkey;
       public            postgres    false    216            �           2606    19031     nivel_contrib nivel_contrib_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.nivel_contrib
    ADD CONSTRAINT nivel_contrib_pkey PRIMARY KEY (id_nivel);
 J   ALTER TABLE ONLY public.nivel_contrib DROP CONSTRAINT nivel_contrib_pkey;
       public            postgres    false    220            �           2606    19006    rol rol_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_pkey PRIMARY KEY (id_rol);
 6   ALTER TABLE ONLY public.rol DROP CONSTRAINT rol_pkey;
       public            postgres    false    215            �           2606    19036    tipo_eval tipo_eval_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.tipo_eval
    ADD CONSTRAINT tipo_eval_pkey PRIMARY KEY (id_tipo_eval);
 B   ALTER TABLE ONLY public.tipo_eval DROP CONSTRAINT tipo_eval_pkey;
       public            postgres    false    221            ~           2606    18997    usuario usuario_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (email);
 >   ALTER TABLE ONLY public.usuario DROP CONSTRAINT usuario_pkey;
       public            postgres    false    214                  x������ � �            x������ � �            x������ � �            x������ � �            x�KL����4����� ��             x������ � �         &   x�+H,�wH�M���K���4426153������� ��     