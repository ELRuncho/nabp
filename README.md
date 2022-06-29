<h1 align="center">NABP Linea de comandos</h1>
<h3 align="center">Mejores practicas para una nueva cuenta de AWS</h3>

## Tabla de Contenido

- 🔭 [Como crear una nueva cuenta](https://github.com/ELRuncho/nabp#como-crear-una-nueva-cuenta)

- 👤 [Crear usuario administrador](https://github.com/ELRuncho/nabp#crear-usuario-administrador)

- 🚀 [Como instalar nabp](https://github.com/ELRuncho/nabp#como-instalar-nabp)

- 👯 [Comandos core](https://github.com/ELRuncho/nabp#comandos-core)

- :eye: [Comandos Monitor](https://github.com/ELRuncho/nabp#comandos-monitor)

- 🤝 [Comandos Network](https://github.com/ELRuncho/nabp#comandos-network)


## Como crear una nueva cuenta
1. Abra la [página de inicio de Amazon Web Services (AWS)](https://aws.amazon.com/).
    ![](./images/awshome.png)
2. Elija Create an AWS Account (Crear una cuenta de AWS).
    **Nota:** Si ha iniciado sesión en AWS recientemente, elija Iniciar sesión en la consola. Si Create a new AWS account (Crear una nueva cuenta de AWS) no es visible, elija primero Sign in to a different account (Iniciar sesión con una cuenta diferente) y, a continuación, Create a new AWS account (Crear una nueva cuenta de AWS).
    ![](./images/email.png)
3. En Root user email address (Email del usuario raíz), escriba su email, edite el nombre de la cuenta de AWS y, a continuación, elija Verify email address (Verificar email). Se enviará un email de verificación de AWS a esta dirección con un código de verificación.

    **Consejo:** En el caso de la dirección de email del usuario raíz, utilice un buzón o una lista de distribución de email de empresa (por ejemplo, administradores.empresa@ejemplo.com) si su cuenta es una cuenta de AWS profesional. Evite utilizar el email de empresa de una persona (por ejemplo, paulo.santos@ejemplo.com). De este modo, su empresa seguirá teniendo acceso a la cuenta de AWS incluso si un empleado cambia de puesto o deja la empresa. La dirección de email se puede utilizar para restablecer las credenciales de la cuenta. Asegúrese de proteger el acceso a estas listas de distribución. No utilice el inicio de sesión del usuario raíz de la cuenta de AWS para sus tareas cotidianas. Es una práctica recomendada habilitar la autenticación multifactor (MFA) en la cuenta raíz para proteger los recursos de AWS.

    **Consejo:** En el caso del Nombre de la cuenta de AWS, utilice un estándar de denominación de cuentas que permita que el nombre de la cuenta sea reconocible en la factura o en la consola de administración de facturación y costos. Si se trata de una cuenta de empresa, considere utilizar el estándar de denominación organización-objetivo-entorno (por ejemplo, EmpresaEjemplo-auditoría-prod). En caso de que sea una cuenta personal, plantéese utilizar el estándar de denominación nombre-apellido-objetivo (por ejemplo, paulo-santos-cuentadeprueba). Puede cambiar el nombre de la cuenta en la configuración de la cuenta después de registrarse. Para obtener más información, consulte ¿Cómo cambio el nombre en mi cuenta de AWS?

### Verifique su email

Ingrese el código que reciba y, a continuación, seleccione Verify (Verificar). El código puede tardar unos minutos en llegar. Compruebe su email y la carpeta de spam para el email de código de verificación.

![](./images/emailcode.png)


### Cree su contraseña

Ingrese su contraseña de usuario raíz, confirme la contraseña de usuario raíz y, a continuación, seleccione Continue (Continuar).

![](./images/password.png)

### Agregue su información de contacto

1. Seleccione Personal (Personal) o Business (Empresa).
    **Nota:** Las cuentas personales y empresariales tienen las mismas características y funciones.
2. Ingrese su información personal o empresarial.
    **Importante:** Para cuentas de AWS empresariales, se recomienda ingresar el número de teléfono de la empresa en lugar de un número de teléfono móvil personal. Configurar una cuenta raíz con una dirección de email o un número de teléfono personales puede provocar que la cuenta no sea segura.
3. Lea y acepte el Contrato de usuario de AWS.
4. Elija **Continuar**.

![](./images/info.png)

Recibirá un email para confirmar que se ha creado su cuenta. Puede iniciar sesión en su nueva cuenta con la dirección de email y la contraseña que utilizó para registrarse. No obstante, no podrá utilizar los servicios de AWS hasta que termine de activar la cuenta.

### Agregue un método de pago

En la página **Información de facturación**, ingrese la información de su método de pago y, a continuación, elija Verify and Add (Verificar y agregar).

Si se está registrando en la India para obtener una cuenta de Amazon Internet Services Private Limited (AISPL), debe proporcionar su CVV como parte del proceso de verificación. Asimismo, es posible que tenga que ingresar una contraseña de un solo uso, en función del banco. AISPL realizará un cargo de 2 rupias indias (INR) en el método de pago como parte del proceso de verificación. AISPL reembolsará las 2 INR una vez que se complete la verificación.

Si desea utilizar una dirección de facturación diferente para la información de facturación de AWS, elija **Use a new address** (Utilizar una nueva dirección). A continuación, elija **Verify and Continue** (Verificar y continuar).

**Importante:** No puede continuar con el proceso de registro mientras no agregue un método de pago válido.

![](./images/creditcard.png)

### Verifique su número de teléfono

1. En la página Confirme su identidad, seleccione un método de contacto para recibir un código de verificación.
    ![](./images/phone.png)
2. Seleccione el país o código de región de su número de teléfono en la lista.
3. Ingrese un número de teléfono móvil en el que se le pueda contactar durante los próximos minutos.
4. Si aparece un CAPTCHA, ingrese el código mostrado y luego envíelo.
5. Transcurridos unos instantes, un sistema automatizado le contactará.
6. Escriba el PIN recibido y luego elija **Continuar**.
    ![](./images/phonecode.png)

### Elija un plan de AWS Support

En la página Seleccione un plan de soporte, elija uno de los planes de soporte disponibles. Para ver la descripción de los planes de soporte disponibles y sus beneficios, consulte Compare los planes de AWS Support.

Elija Finalizar inscripción.

![](./images/support.png)

### Espere a que se active la cuenta

Después de elegir un plan de Support, una página de confirmación le indica que su cuenta está siendo activada. Por lo general, las cuentas se activan en unos pocos minutos, aunque el proceso puede tardar hasta 24 horas.

![](./images/complete.png)

Puede iniciar sesión en su cuenta de AWS durante ese tiempo. La página de inicio de AWS puede mostrar el botón **Completar el inicio de sesión** durante ese plazo de tiempo, incluso si ya ha completado todos los pasos del proceso de inicio de sesión.

Cuando su cuenta se haya activado por completo, recibirá un email de confirmación. Compruebe su email y la carpeta de spam para encontrar el email de confirmación. Después de recibir este email, tendrá acceso completo a todos los servicios de AWS.

## Crear usuario administrador

### Para crear uno o varios usuarios de IAM (consola)

1. Inicie sesión en la AWS Management Console y abra la consola de IAM en [link](https://console.aws.amazon.com/iam/)
    ![](./images/slectIAM.png)
2. En el panel de navegación, elija Usuarios y, a continuación, elija Agregar usuarios.
    ![](./images/users.png)
3. Escriba el nombre de usuario del nuevo usuario. Este es el nombre de inicio de sesión para AWS. Si quiere agregar varios usuarios, seleccione Add another user (Agregar otro usuario) para cada usuario adicional y escriba sus nombres de usuario. Puede añadir hasta 10 usuarios al mismo tiempo.
    ![](./images/userdata.png)
4. Seleccione el tipo de acceso que tendrá este conjunto de usuarios. Puede seleccionar el acceso mediante programación, el acceso a la AWS Management Console, o ambos.

    * Seleccione **Acceso mediante programación** si los usuarios necesitan obtener acceso a la API, la AWS CLI o Tools for Windows PowerShell. Esto crea una clave de acceso para cada usuario nuevo. Puede ver o descargar las claves de acceso cuando llegue a la página Final.

    * Seleccione **AWS Management Console access** (acceso a la consola) si los usuarios necesitan obtener acceso a la AWS Management Console. Esto crea una contraseña para cada usuario nuevo.

    - En **Console password (Contraseña de la consola)**, elija una de las opciones siguientes:

        - **Autogenerated password (Contraseña generada automáticamente)**. Cada usuario obtiene una contraseña generada de forma aleatoria que cumple la política de contraseñas de cuentas. Puede ver o descargar las contraseñas cuando llegue a la página Final.

        - **Custom password (Contraseña personalizada)**. A cada usuario se le asigna la contraseña que se escribe en el cuadro.

    - (Opcional) Le recomendamos que seleccione **Require password reset (Requerir restablecimiento de contraseña)** para asegurarse de que los usuarios estén obligados a cambiar su contraseña la primera vez que inicien sesión.


5. Elija Next: Permissions (Siguiente: Permisos).

6. En la página Set permissions (Establecer permisos), especifique la forma en que quiera asignar permisos a este conjunto de nuevos usuarios. Elija una de las siguientes tres opciones:
    
    ![](./images/policy.png)

    - **Add user to group (Añadir un usuario al grupo)**. Elija esta opción si desea asignar los usuarios a uno o a varios grupos que ya tienen políticas de permisos. IAM muestra una lista de los grupos de la cuenta, junto con sus políticas asociadas. Puede seleccionar uno o varios grupos existentes o elegir Create group (Crear grupo) para crear un grupo nuevo. Para obtener más información, consulte Cambio de los permisos de un usuario de IAM.

    - **Copy permissions from existing user (Copiar permisos de un usuario existente)**. Elija esta opción para copiar todas las suscripciones a grupos, las políticas administradas asociadas, las políticas insertadas integradas y los límites de permisos de un usuario existente en los usuarios nuevos. IAM muestra una lista de los usuarios de la cuenta. Seleccione el usuario cuyos permisos se acerquen lo máximo posible a las necesidades de los usuarios nuevos.

    - **Attach existing policies directly (Asociar las políticas existentes directamente)**. Elija esta opción para ver una lista de las políticas administradas por AWS y de las políticas administradas por el cliente de la cuenta. Seleccione las políticas que desea asociar a los nuevos usuarios o elija Create policy (Crear política) para abrir una nueva pestaña del navegador y crear una nueva política desde cero. Para obtener más información, consulte el paso 4 del procedimiento Crear políticas de IAM. Una vez creada la política, cierre la pestaña y vuelva a la pestaña original para añadir la política al nuevo usuario. Como práctica recomendada, es conveniente que primero asocie sus políticas a un grupo y después haga a los usuarios miembros de los grupos adecuados.

7. (Opcional) Configure un límite de permisos. Esta es una característica avanzada.

    Abra la sección **Set permissions boundary (Configurar límite de permisos)** y elija **Utilice a permissions boundary to control the maximum user permissions (Utilizar un límite de permisos para controlar los permisos que puede tener el usuario como máximo)**. IAM muestra una lista de las políticas administradas por AWS y de las políticas administradas por el cliente de la cuenta. Seleccione la política que desea usar para el límite de permisos o elija **Create policy (Crear política)** para abrir una pestaña nueva del navegador y crear una política nueva desde cero. Para obtener más información, consulte el paso 4 del procedimiento Crear políticas de IAM. Una vez creada la política, cierre la pestaña y vuelva a la pestaña original para seleccionar la política que va a usar para el límite de permisos.

8. Elija Next: Tags (Siguiente: Etiquetas).

9. (Opcional) Añadir metadatos al rol asociando las etiquetas como pares de clave-valor. Para obtener más información acerca del uso de etiquetas en IAM, consulte Etiquetado de recursos de IAM.
    ![](./images/tags.png)

10. Elija **Next: Review (Siguiente. Revisar)** para ver todas las opciones que ha realizado hasta este punto. Cuando esté listo para continuar, elija Create user **(Crear usuario)**.
    ![](./images/review.png)

11. Para ver las claves de acceso de los usuarios (los ID de las claves de acceso y las claves de acceso secretas), elija **Show (Mostrar)** junto a cada contraseña y clave de acceso secreta que desee ver. Para guardar las claves de acceso, elija **Download .csv (Descargar archivo .csv)** y, a continuación, guarde el archivo en un lugar seguro. 

    ![](./images/downloadkeys.png)

    **importante:**
        Esta es la única oportunidad que tiene para ver o descargar las claves de acceso secretas, y debe proporcionar dicha información a los usuarios para que puedan usar la API de AWS. Guarde el nuevo ID de clave de acceso del usuario y la clave de acceso secreta en un lugar seguro. No volverá a tener acceso a la clave de acceso secreta después de este paso.

    ![](./images/final.png)

12. Proporcione a cada usuario sus credenciales. En la página final puede elegir Send email (Enviar correo electrónico) junto a cada usuario. Su cliente de correo local se abrirá con un borrador que puede personalizar y enviar. La plantilla de correo electrónico contiene los detalles siguientes por cada usuario:

    - Nombre de usuario

    - URL de la página de inicio de sesión de la cuenta. Utilice el ejemplo siguiente y realice la sustitución con el número de ID o de alias de cuenta correcto:

        `https://AWS-account-ID or alias.signin.aws.amazon.com/console`

    Para obtener más información, consulte [Cómo inician sesión los usuarios de IAM en AWS.](https://docs.aws.amazon.com/es_es/IAM/latest/UserGuide/id_users_sign-in.html) 

## Como instalar nabp

### Prerequisitos

1. Python3 o superior y pip [Python](https://www.python.org/downloads/)
2. AWS CLI [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
    - Al instalar la linea de comandos,usando el comando `aws configure`, usa las llaves obtenidas del usuario admin creado anteriormente. 
        ```
            $ aws configure
            AWS Access Key ID: <Access key del usario>
            AWS Secret Access Key: <Access key del usario>
            Default region name: us-east-1 <us-east-1 es la region por defecto>
        ```
**Importante:**
    En Windows, si python o el AWS cli, una vez instalados no se encuentran desde el command prompt se deben agregar a la variable de ambiente PATH.
    Para encontrar el folder que contiene el awscli o python puede usar el comando `where`:

        
        C:\> where /R c:\ <paquete aws o python/py>

### No tienes un equipo Linux o tu computador tiene controles que te impiden instalar? 
En este caso puedes hacer uso de *AWS CLOUDSHELL* para poder tener un ambiente de consola sin tener que desplegar recursos adicionales.

Para usar CloudShell solo debes buscar el servicio en la consola:
![](./images/cloudshellSearch.png)

Una vez estes en CloudShell puedes configurar aws cli que ya viene instalado, asi como python

![](./images/cloudshell.png)

### Instalacion

1. Descarga nabp desde github ya sea descargando el zip o clonando el repositorio

    `$ git clone https://github.com/ELRuncho/nabp.git`

2. Ingresa al folder:

    `$ cd nabp`

3. Instala nabp usando pip:

    `$ pip3 install .`

4. Confirma la instalacion:

    `$ nabp --help`

    - Si se instalo exitosamente deberias ver el siguiente output:
        ```
            Usage: nabp [OPTIONS] COMMAND [ARGS]...

            Options:
                --profile TEXT  perfil preferido de awscli
                --help          Show this message and exit.

            Commands:
                core     Comandos core
                network  Comandos networking
        ```
5. (OPTIONAL) una vez instalado napb puedes definir el perfil del awscli para usar con nabp usando la opcion `--profile`

    `$ nabp --profile <nombre perfil awslcli>`

    Si no se define ningun perfil con la opcion `--profile` nabp usa el perfil default de awscli

## Comandos Core

Estos comandos crean configuracion base para la cuenta

### seguridad

Este comando activa **Access Analyzer** que automaticamente analiza las politicas creadas de IAM basandose en los patrones de uso de los usarios y recursos y alerta en caso de que las poiticas sean muy holgadas y violen el principio de menor privilegio.

Este comando tambien crea cuatro grupos de usuarios de IAM les asigna permisos especificos para cada grupo y tambien crea un usuario en cada grupo. Los grupos que crea son los siguientes:

- **Administradores:** Grupo para Administradores, este grupo tiene permisos completos de administrador para aws
- **Developers:** Grupo para Desarrolladores, este grupo tiene permisos de power user, permite crear recursos pero no modificar politicas de seguridad ni informacion de billing
- **Auditores:** Grupo para Auditores, este grupo tiene permisos de solo lectura, pensado para auditores que requieran poder ver y revisar recursos, politicas, configuraciones, etc. Pero no permite realizar ningun cambio
- **Finanzasz:** Grupo para Finanzas, este grupo tiene permisos para acceder solamente la informacion de facturacion y costos asi como poder crear presupuestos

Este comando tiene las siguientes opciones (ninguno es requerido para poder ejecutar el comando):

- `--analyzer_nombre`: Nombre personalizado para al Access Analyzer 
- `--nombre_admin_g`: Nombre personalizado para el grupo de administradores
- `--nombre_dev_g`: Nombre personalizado para el grupo de desarrolladores
- `--nombre_audit_g`: Nombre personalizado para el grupo de auditores
- `--nombre_fin_g`: Nombre personalizado para el grupo de finanzas

**Ejemplo:**

Sin opciones:

`$ nabp core seguridad`

Con opciones:
    
`$ nabp core seguridad --analyzer_nombre miAnalyzer --nombre_admin_g AdminG --nombre_dev_g Devs`

### presupuesto

Este comando crea un presupuesto en la cuenta de aws y dos alertas, una al cumplirse el 60% del presupuesto en consumo y otra al cumplirse el 90%. Estas alertas se enviaran al email definido en el comando

Este comando tiene las siguientes opciones:

- `--nombre`: Nombre personalizado de el presupesto 
- `--monto` **(requerido)**: Monto maximo del presupuesto, el valor esta dado en dolares (USD)
- `--email` **(requerido)**: Email al que se enviaran las alertas

**Ejemplo:**

Sin nombre:

`$ nabp core presupuesto --monto 200 --email admin@empresa.com`

Con nombre:

`$ nabp core presupuesto --nombre miPresupuesto --monto 200 --email admin@empresa.com`

## Comandos Monitor

### trail

Este comando crea un bucket para almacenar logs de cloudtrail y habilita cloudtrail para todas las regiones dentro de tu nueva cuenta.

Este comando tiene las siguientes opciones:

- `--nombre`: Esta opcion permite especificar el nombre de el trail a crearse en AWS CloudTrail, el nombre default es *nabp-trail*

**Ejemplo:**

Sin opciones:

`$ nabp monitor trail`

Nombre custom para el trail:

`$ nabp monitor trail --nombre mitrail `


### config

## Comandos Network

### crear

Este commando crea una VPC con tres subnets publicas tres subnets privadas, IGW, un NatGateway y las tablas de enrutamiento y rutas necesarias.

Este comando tiene las siguientes opciones:

- `--rango`: Esta opcion permite especificar el rango CIDR de la VPC en formato *X.X.X.X/X*, su valor por defecto es 10.0.0.0/16
- `--region`: Esta opcion permite especificar la region donde se quiere desplegar la vpc

**Ejemplo:**

Sin opciones:

`$ nabp network crear`

Con opciones:

`$ nabp network crear --rango 172.0.0.0/16`

<h3 align="left">Connect with me:</h3>
<p align="left">
<a href="https://www.linkedin.com/in/rafael-hernando-franco/" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/linked-in-alt.svg" alt="rafael" height="30" width="40" /></a>
</p>

<h3 align="left">Languages and Tools:</h3>
<p align="left"> <a href="https://aws.amazon.com" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" alt="aws" width="40" height="40"/> </a> <a href="https://www.gnu.org/software/bash/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/gnu_bash/gnu_bash-icon.svg" alt="bash" width="40" height="40"/> </a> <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> <a href="https://www.linux.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg" alt="linux" width="40" height="40"/> </a>  <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>  </p>