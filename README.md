Gin Rummy Engine
=======================

This repository contains the backend engine for a Gin Rummy game implemented using Flask. The engine handles game logic, user management, and API endpoints required to run and manage a Gin Rummy game server.

Features
--------

*   **User Authentication**: Manages user login, registration, and authentication using JWT.
*   **Match Management**: Create and manage Gin Rummy matches, including handling players, rounds, and turns.
*   **Card Management**: Handles all card-related operations, including drawing cards, managing hands, and playing melds.
*   **Scoring System**: Implements the scoring rules of Gin Rummy, including point calculation for melds and penalties.
*   **API Endpoints**: Provides RESTful endpoints for interaction with the Gin Rummy game engine.

Getting Started
---------------

### Prerequisites

*   Python 3.8 or higher
*   MySQL Server
*   Git
*   Nginx (optional, for production deployment)

### Installation

1.  **Clone the repository**

    ```bash
    git clone git@github.com:your-username/ginrummy-engine.git
    cd ginrummy-engine
    ```

2.  **Configure the database**

    Run the database installation script, passing `--host`, `--user`, `--database`, and `--password` as arguments:

    ```bash
    python3 setup/install_database.py --host=localhost --user=root --database=GinRummy --password=your-password
    ```

3.  **Run the application**

    ```bash
    python3 -m api.api
    ```

    The API will be accessible at `http://localhost:5000`.


### Deployment

For production deployment, you can use the provided `setup/server_installation.sh` script to automate the setup with Nginx and Gunicorn.

```bash
cp setup/server_installation.sh ~/setup-engine.sh
chmod +x ~/setup-engine.sh
~/setup-engine.sh
```

This will:

*   Ensure the script is executed with root privileges, as required for system-level configurations.
*   Prompt you to enter your domain name and check if an SSL certificate is already installed. If not, it will automatically obtain one using Certbot.
*   Generate an SSH key pair if it does not already exist, and assist you in adding it to your GitHub account for secure access to your repositories.
*   Add GitHub's SSH key fingerprints to the known hosts to prevent verification issues during Git operations.
*   Update the server's package lists, upgrade all packages to their latest versions, and install essential software packages, including Python, pip, Git, MySQL server, Nginx, Certbot, and more.
*   Set up MySQL, including generating a secure root password, configuring MySQL for optimal performance, and securing the installation by removing unnecessary users and databases.
*   Add swap space if none exists, enhancing server performance by providing additional virtual memory.
*   Clone or update the `ginrummy-engine` repository from GitHub, set up a Python virtual environment, and install all necessary Python dependencies for the application.
*   Install and configure the application database, including setting up the required tables and prompting you to create application users with secure passwords.
*   Configure Gunicorn as a systemd service to run the Flask application, ensuring it starts on boot and is properly logged.
*   Set up Nginx as a reverse proxy to manage incoming web traffic, handle SSL termination, and redirect HTTP traffic to HTTPS for improved security.
*   Enable and start the configured services (Nginx and Gunicorn), ensuring your web application is fully operational and secure.


Game Rules
----------

### Objective

The goal of the game is to accumulate the highest number of points across multiple rounds. You earn points by playing melds and lose points for cards left in your hand at the end of a round.

### Scoring

*   **Ace:** 15 points
*   **10, Jack, Queen, King:** 10 points
*   **2–9:** Points equal to their rank (e.g., 2 is worth 2 points)

### Playing melds

Melds, which are essential for scoring, can only be played starting from a player's second turn in the round. This means no melds can be played during the first turn of any player within a new round.

#### Types of melds
*   **Set:** 3 or 4 cards of the same rank.
*   **Run:** At least 3 consecutive cards of the same suit. Aces can be high or low (e.g., Queen, King, Ace or Ace, 2, 3). However, a run cannot "loop around" (e.g., King, Ace, 2 is not allowed).

### Turn sequence

1.  **Draw a card:**
    *   You must start your turn by drawing a card from either the stock pile or the top of the discard pile. In some cases, you can draw multiple cards from the discard pile. See: [_Special abilities_](#special-abilities).
    *   If the discard pile is empty, you must draw from the stock pile.
    *   If the stock pile is empty, you may either draw from the discard pile or turn the discard pile over to create a new stock pile and draw the top card.
2.  **Play melds:**
    *   After the first rotation, you can play a meld. Once you've played a meld, you gain additional abilities. See: [_Special abilities_](#special-abilities).
3.  **Discard a card:**
    *   End your turn by discarding a card to the top of the discard pile. This is done in a way that keeps all previously discarded cards visible.
    *   If discarding leaves you with no cards in your hand, the round ends.

### Special abilities

Once you have played your first meld in a round, you gain the following special abilities:

#### Extending melds
*   You may add cards to an existing meld to make it larger. This can include adding the fourth card to a set of three or adding any number of consecutive cards to an existing run.
*   You can extend all melds, regardless of who originally played them.
*   You receive points only for the cards you contributed towards a meld.

#### Drawing multiple cards
*   At the start of your turn, you can choose to draw multiple cards from the discard pile.
*   You must nominate at least one of these cards to immediately play as part of a new or extended meld.
*   You may nominate multiple cards from the discard pile, and may also select cards from your own hand, for combined use when playing or extending a meld.
*   Any other cards above the nominated cards are added to your hand, after which you continue your turn as normal.

### End of a round

A round ends only when a player discards their last card. As such, you cannot play cards in a way that leaves you with an empty hand, prior to discarding.

Each remaining player is deducted points equal to the value of the cards still in their hand. This can result in a negative score.

A new round may begin immediately, with the first turn going to the next player clockwise from the one who started the previous round.

Use these rules to strategize your moves and outplay your opponents!

Contributing
------------

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

License
-------

This project is licensed under the MIT License. See the `LICENSE` file for more details.
