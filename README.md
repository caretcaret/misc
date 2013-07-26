misc v0.1
====

Small, miscellaneous pieces of code that don't deserve their own repository (yet?).

WARNING: Some code may be broken, unfinished, or not work as intended. Run/read at your own risk.

What is everything?
====

*almamater-xkcd* (Apr 2013) :: Haskell program written for the xkcd hash challenge. It successfully calculates the hash of a string made from a subset of characters [A-Za-z0-9.]\*. Does not implement brute-force checking.

*caretbot* (Dec 2012) :: Python irc bot written for xchat. It has a list of triggers and responses; when someone writes the trigger string, caretbot responds with the corresponding response. Users in the channel can change triggers and responses interactively.

*didigetin* (Feb 2012) :: Python Pyramid minimalist site for announcing college decision statuses. Bug: does not use unique salts for each user.

*food-club* (Jul 2012) :: Python script to construct and evaluate bets for the Neopets Food Club game. Bugs: somewhat inefficient implementation, does not read data from files or neopets in real time.

*hanzi-order* (Apr 2013) :: Python script to investigate the most optimal order to learn the Chinese characters, based on the cumulative number of character compounds known. Bug: main function is inefficient, does not actually cache results inside the build directory.

*lilypad* (Jan 2013) :: Custom CSS styling and HTML templates for the gitit wiki. Feature: reveals a rendering bug in webkit.

*lmc* (Jan 2012) :: Python Pyramid site for managing the Leland Math Club with styling built from scratch. Currently features account registration, news posts, file upload/download. Bugs: many features unimplemented, does not use unique salts for each user password.

*misinterpreted* (Jun 2011) :: Android application implementing Broken Picture Telephone, with drawing support. Gameplay on the same device is implemented. Bugs: Many desired features unimplemented.

*nomic* (Nov 2012) :: Markdown file including initial rules for Nomic. Currently no programmatic component; maybe later as a webapp.

*petbot* (Jan 2013) :: Multithreaded reddit bot in python. Designed to be modular. The logic is there, but interaction with reddit is incomplete. TODO: use the PRAW library.

*rps101* (2010?) :: Python + wx implementation of Rock-Paper-Scissors 101. Contains data files and images from the creator. Incomplete.

*shamir* (Aug 2012) :: Python script implementing Shamir's secret sharing and Lagrange interpolation, used for the CMU 15-151 puzzle.

*subreddit-list* (Oct 2012) :: Python script utility to read a json file representing list of subreddits and format it prettily in HTML.

*voltorb-flip* (Dec 2012) :: Python script to evaluate a game of Voltorb Flip on Pokémon HeartGold/SoulSilver by printing out result probabilities. Bug: does not take input from a file.

