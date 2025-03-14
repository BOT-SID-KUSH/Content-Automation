import os

def get_words_from_grid(grid, puzzle_id):
    """Extract words and their metadata from the grid"""
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    words = []

    # Find horizontal words
    for row in range(height):
        word = ""
        start_col = -1
        for col in range(width):
            if grid[row][col] != '.':
                if start_col == -1:
                    start_col = col
                word += grid[row][col]
            elif word:  # Word ended and has length > 1
                if word != '_':  # Skip if word is just underscore
                    words.append({
                        'puzzleId': puzzle_id,
                        'word': word,
                        'row': row,
                        'column': start_col - 1,  # Clue position is one before word
                        'direction': 'across',
                        'clueContent': 'NA'
                    })
                word = ""
                start_col = -1
            else:
                word = ""
                start_col = -1
        # Check for word at end of row
        if word and word != '_':  # Skip if word is just underscore
            words.append({
                'puzzleId': puzzle_id,
                'word': word,
                'row': row,
                'column': start_col - 1,
                'direction': 'across',
                'clueContent': 'NA'
            })

    # Find vertical words
    for col in range(width):
        word = ""
        start_row = -1
        for row in range(height):
            if grid[row][col] != '.':
                if start_row == -1:
                    start_row = row
                word += grid[row][col]
            elif word:  # Word ended and has length > 1
                if word != '_':  # Skip if word is just underscore
                    words.append({
                        'puzzleId': puzzle_id,
                        'word': word,
                        'row': start_row - 1,  # Clue position is one above word
                        'column': col,
                        'direction': 'down',
                        'clueContent': 'NA'
                    })
                word = ""
                start_row = -1
            else:
                word = ""
                start_row = -1
        # Check for word at end of column
        if word and word != '_':  # Skip if word is just underscore
            words.append({
                'puzzleId': puzzle_id,
                'word': word,
                'row': start_row - 1,
                'column': col,
                'direction': 'down',
                'clueContent': 'NA'
            })
    
    return words

def read_grid_files():
    grid_dir = "grids"
    all_words = []
    
    # Check if directory exists
    if not os.path.exists(grid_dir):
        print(f"Error: {grid_dir} directory not found")
        return all_words

    # Read all .txt files in grids directory and sort by filename
    filenames = sorted([f for f in os.listdir(grid_dir) if f.endswith('.txt')])
    
    for filename in filenames:
        filepath = os.path.join(grid_dir, filename)
        try:
            with open(filepath, 'r') as f:
                grid = [line.strip() for line in f.readlines()]
                puzzle_id = os.path.splitext(filename)[0]
                words = get_words_from_grid(grid, puzzle_id)
                all_words.extend(words)
        except Exception as e:
            print(f"Error reading {filename}: {str(e)}")
            continue
    
    # Write results to TSV file
    with open('grid_clues.tsv', 'w') as f:
        # Write header
        f.write('puzzleId\tword\trow\tcolumn\tdirection\tclueContent\n')
        
        # Write data
        for word in all_words:
            f.write(f"{word['puzzleId']}\t{word['word']}\t{word['row']+1}\t{word['column']+1}\t{word['direction']}\t{word['clueContent']}\n")
    
    return all_words

read_grid_files()