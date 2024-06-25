# LogBook
#### Descrição: 
Desenvolvi este livro de registro com base em minha experiência profissional em uma grande empresa que tinha mais de 2.000 funcionários.
Em empresas com um grande número de funcionários, uma das maiores dificuldades é comunicar o que e como cada atividade deve ser realizada. Portanto, o objetivo deste livro de registro é facilitar a gestão das atividades realizadas por funcionários de diferentes setores dentro da empresa. Aqui o gerente e os funcionários podem se registrar no aplicativo onde o gerente terá autorização para adicionar tarefas e definir um prazo para sua conclusão, e tanto o gerente quanto o funcionário poderão completá-las, sendo lembrados diariamente se a tarefa está no prazo ou atrasada. O programa também registra qual funcionário foi responsável por completar as tarefas, mantendo o gerente informado sobre a produtividade de sua equipe.


## Pasta de Templates
#### apology.html: 
Retorna aos usuários do aplicativo os possíveis erros destacados ao usar o programa.

#### approval_result.html: 
Apenas um modelo que direciona a pessoa responsável pelo servidor e informa a eles sua decisão de aprovar ou não o registro de um novo usuário como administrador.

#### description.html: 
Mostra a descrição mais específica das atividades a serem realizadas, como o que e como deve ser feito.

#### history.html: 
Mostra o histórico das atividades já realizadas, se foram realizadas dentro do prazo ou não e também quem foi responsável por realizá-las.

#### index.html: 
A página inicial exibe tarefas em andamento, ou seja: tarefas que ainda não foram concluídas e podem ser acompanhadas por todos, facilitando assim saber o que precisa ser feito.

#### layout.html: 
Layout suportado pelo Bootstrap e usado para todos os outros modelos.

#### leader.html: 
Página restrita aos administradores. É possível adicionar tarefas e seus respectivos prazos, além de informar na descrição o que e como deve ser feito com mais detalhes.

#### login.html and register.html: 
Modelos para registro e login de usuário. Ao se registrar, você terá a opção de solicitar o registro como administrador enviando um e-mail para a pessoa responsável pelo servidor solicitando sua liberação para que você possa adicionar tarefas.


## Static folder: 
Contém o arquivo style.css que cuida do estilo do aplicativo e também o ícone de livros usado no cabeçalho do layout.


#### database.db: 
Banco de dados contendo as 3 tabelas usadas para armazenar os dados fornecidos pelo usuário e que garantem o funcionamento do aplicativo. Contém informações como ID dos usuários, seu nome de usuário, sua senha (obviamente criptografada), a descrição das tarefas, seu título, os prazos exigidos pelo administrador, etc.

#### app.py: 
Arquivo onde nosso código foi escrito e que garante o dinamismo e funcionamento da página através de suas funções que permitem registro, login, armazenamento de informações, envio de e-mails, links, etc. Foi descrito em Python com a ajuda do framework Flask e a importação de outras bibliotecas.




# LogBook
## Description: 
I developed this logbook based on my professional experience in a large company that had more than 2,000 employees.
In companies with a large number of employees, one of the biggest difficulties is communicating what and how each activity should be carried out. Therefore, the objective of this logbook is to facilitate the management of activities carried out by employees from different sectors within the company. Here the manager and employees can register on the application where the manager will have the authorization to add tasks and set a deadline for their completion and both manager and employee will be able to complete them, being reminded daily if the task is on time or late. The program also records which employee was responsible for completing the tasks, keeping the manager informed about the productivity of his staff.


## Templates Folder
#### apology.html: 
Returns to application users the possible errors highlighted when using the program.

#### approval_result.html: 
Just a template that directs the person responsible for the server and informs them of their decision to approve or not the registration of a new user as an administrator.

#### description.html: 
Shows the most specific description of the activities to be carried out, such as what and how it should be done.

#### history.html: 
Shows the history of activities already carried out, whether they were carried out on time or not and also who was responsible for carrying them out.

#### index.html: 
The homepage displays tasks in progress, that is: tasks that have not yet been completed and can be followed by everyone, so it is easy to know what needs to be done.

#### layout.html: 
Layout supported by Bootstrap and used for all other templates.

#### leader.html: 
Page restricted to administrators. It is possible to add tasks and their respective deadlines, in addition to informing in the description what and how should be done in more detail.

#### login.html and register.html: 
Templates for user registration and login. When registering, you will have the option to request registration as an administrator by sending an email to the person responsible for the server requesting your release so you can add tasks.


## Static folder: 
Contains the style.css file that takes care of the application's style and also the books icon used in the layout header.

#### database.db: 
database containing the 3 tables used to store the data provided by the user and which guarantee the operation of the application. It contains information such as the users' ID, their username, their password (obviously encrypted), the description of the tasks, their title, the deadlines required by the administrator, etc.

#### app.py: 
file where our code was written and which guarantees the dynamism and functioning of the page through its functions that allow registration, login, storage of information, sending emails, links, etc. It was described in Python with the help of the Flask framework and the import of other libraries.