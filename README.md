# AI and ML first steps

Repository consists of 5 folders: Lab01-5. Each of them contains a solution to a specific problem:

## Lab01 - Optimization of Path Finding with Dijkstra's, A*, and Tabu Search Algorithms

Lab01 focuses on optimizing the process of finding the best path using Dijkstra's, A*, and Tabu Search algorithms, all based on the MPK Wrocław (public transport) timetable. The primary goal is to develop a program that efficiently calculates the most optimal route between two specified stations within the public transport network.

### Technologies Used:

- **Python:** For the implementation of the path finding algorithms and data processing.
- **Graph Data Structure:** For representing the public transport network as a graph.
- **Dijkstra's Algorithm:** For finding the shortest path between stations.
- **A* Algorithm:** For heuristic-based path finding to improve search efficiency.
- **Tabu Search Algorithm:** For optimizing and refining the path found by the other algorithms.
- **Data Parsing and Handling:** For extracting information from the MPK Wrocław timetable data.
- **Data Visualization:** For presenting the optimal path and connections in a user-friendly manner.

The final result of this project is a program that takes user input for the starting and ending stations and returns a list of connections and transfers, similar to the navigation experience provided by popular platforms like Google Maps.

 - - -

## Lab02 - Zero-Sum Game Playing Algorithms

Lab02 focuses on the implementation of zero-sum game playing algorithms with a specific application to the game of REVERSI (also known as Othello). In the game of REVERSI, two players compete on an 8x8 board, with each player having pieces of their color. The goal is to have the majority of the board covered with one's color by the end of the game.

The project involves creating an intelligent bot that can play REVERSI against human players or other bots. The bot's intelligence is achieved by utilizing the MIN-MAX algorithm with alpha-beta pruning. The MIN-MAX algorithm explores the game tree to evaluate the possible moves and outcomes based on a heuristic evaluation function. Alpha-beta pruning optimizes the search by eliminating branches that are unlikely to lead to better outcomes.

The bot's intelligence allows it to make strategic decisions and anticipate the opponent's moves, making it a formidable player in the game of REVERSI.

### Extended Technologies Used:

- **Python:** For the implementation of the REVERSI game and the bot.
- **Object-Oriented Programming (OOP):** Concepts for organizing the game logic and bot behavior.
- **Heuristic evaluation functions:** To assess the desirability of board states during the game.
- **Alpha-beta pruning technique:** For optimizing the search in the game tree.
- **Version control tools like Git:** For collaborative development and managing the project's source code.

This project showcases the application of game theory and artificial intelligence techniques in building intelligent game-playing agents. The combination of Python and relevant libraries enables efficient development and visualization of the REVERSI game and the bot's decision-making process. The use of version control ensures proper project management and collaboration among developers.
 - - -

## Lab03 - Semantic Network and Rule Implementation in Prolog

Lab03 involves the implementation of a semantic network and rules in Prolog. The objective is to create a program that can reason about a given device (in this case, a washing machine) and its different sections with potential problems.

### Technologies Used:

- **Prolog:** For the implementation of the semantic network and logical reasoning.
- **Semantic Network Representation:** For organizing knowledge about the device and its sections.
- **Rule-Based System:** For encoding rules and inferences to deduce possible causes and solutions to problems.
- **CLI:** To interact with the program and input the problematic section of the device.
- **Logical Querying:** For asking questions and obtaining logical answers based on the semantic network and rules.
- **Data Parsing and Handling:** For managing input and processing knowledge about the device and its sections.
- **Error Handling:** For managing unexpected inputs and providing informative responses to users.

The program takes as input the problematic section of the device and uses the semantic network and rules to deduce possible causes and solutions. The implementation demonstrates the power of logic-based reasoning and the effectiveness of Prolog as a language for representing and reasoning about knowledge.
 - - -
## Lab04 - Glass Classification with Machine Learning

Lab04 involves the classification of glass based on its chemical composition using Machine Learning techniques. The primary objective is to build a model that can accurately classify the type of glass based on its chemical parameters. The dataset consists of samples of different types of glass, each described by the amounts of various chemical elements present in the glass.

### Technologies Used:

- **Python:** For data preprocessing, model training, and evaluation.
- **scikit-learn library:** For implementing Machine Learning algorithms and data processing.
- **pandas library:** For data manipulation and analysis.
- **matplotlib and seaborn libraries:** For data visualization and analysis.
- **Jupyter Notebook:** For interactive development and analysis.
- **Machine Learning Algorithms (e.g., SVM, Random Forest, Gradient Boosting):** For training the classification model.
- **Model Evaluation Metrics (e.g., accuracy, precision, recall, F1-score):** For assessing the model's performance.
- **Data Preprocessing Techniques (e.g., feature scaling, transformation):** For preparing the data for model training.

The project begins with data preprocessing, where features are scaled and transformed appropriately. Then, a Machine Learning model is trained on the preprocessed data. The model's performance is evaluated using various metrics like accuracy, precision, recall, and F1-score.

The final result is a well-performing classification model that can accurately classify the type of glass based on its chemical composition.
 - - -
## Lab05 - Joke Humor Prediction using Neural Networks

Lab05 focuses on predicting the humor level of jokes based on historical user ratings. The dataset contains a collection of jokes along with user ratings of their perceived humor. The primary goal is to build a Multilayer Perceptron (MLP) model, a type of neural network, that can predict the humor rating of jokes for new, unseen jokes.

### Technologies Used:

- **Python:** For data preprocessing, model construction, and evaluation.
- **Keras or TensorFlow:** For building and training the neural network.
- **pandas library:** For data manipulation and analysis.
- **matplotlib and seaborn libraries:** For data visualization and analysis.
- **Jupyter Notebook:** For interactive development and analysis.
- **Machine Learning with Neural Networks (MLP):** For building the humor prediction model.
- **Data Preprocessing Techniques (e.g., feature scaling, transformation):** For preparing the data for model training.
- **Hyperparameter Tuning:** For optimizing the model's performance.
- **Cross-Validation:** For robust model evaluation.

The project starts with data preprocessing, where the data is cleaned, and appropriate features are extracted. Then, an MLP model is constructed using Keras or TensorFlow, and the model is trained on the processed data. Hyperparameter tuning and cross-validation are performed to optimize the model's performance.

The final result is a trained MLP model capable of predicting the humor ratings for new jokes, based on previous user ratings.
