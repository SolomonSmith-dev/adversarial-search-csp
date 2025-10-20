#!/bin/bash
# CSE 5120 Homework 2 - Submission Package Builder
# Creates a clean submission ZIP for Canvas upload

set -e  # Exit on error

echo "🎓 CSE 5120 Homework 2 - Building Submission Package"
echo "═══════════════════════════════════════════════════"
echo ""

# Clean and rebuild submission folder
echo "📁 Creating fresh submission folder..."
rm -rf submission
mkdir -p submission/homework_2_code_files submission/csp

# Copy required files
echo "📋 Copying code files..."
cp homework_2_code_files/GameStatus_5120.py submission/homework_2_code_files/
cp homework_2_code_files/multiAgents.py submission/homework_2_code_files/
cp homework_2_code_files/large_board_tic_tac_toe.py submission/homework_2_code_files/

cp csp/knights_csp.py submission/csp/
cp csp/vehicles_csp.py submission/csp/

cp requirements.txt submission/

# Create submission README
cat > submission/README.md << 'EOF'
# CSE 5120 - Homework 2 Submission

## How to Run

### Tic-Tac-Toe GUI
```bash
pip install -r requirements.txt
python3 homework_2_code_files/large_board_tic_tac_toe.py
```

### CSP Solvers
```bash
python3 csp/knights_csp.py
python3 csp/vehicles_csp.py
```

## Requirements
- Python 3.x
- pygame
- numpy

## Authors
Solomon Smith (008679600)  
Alexander Masley (008968356)
EOF

echo "✅ Code files copied"
echo ""

# Check for Report.pdf
if [ -f "IMPLEMENTATION_SUMMARY.md" ]; then
    if [ -f "Report.pdf" ]; then
        echo "✅ Found Report.pdf, copying to submission..."
        cp Report.pdf submission/
    else
        echo "⚠️  Report.pdf not found. You need to:"
        echo "   1. Convert IMPLEMENTATION_SUMMARY.md to PDF"
        echo "   2. Save as Report.pdf in this directory"
        echo "   3. Run this script again"
        echo ""
        echo "Quick conversion options:"
        echo "   • VS Code: Install 'Markdown PDF' extension"
        echo "   • Command line: pandoc IMPLEMENTATION_SUMMARY.md -o Report.pdf"
        echo ""
        exit 1
    fi
fi

# Remove old ZIP
[ -f "CSE5120_HW2_Submission.zip" ] && rm CSE5120_HW2_Submission.zip

# Create ZIP
echo "📦 Creating ZIP file..."
cd submission && zip -r ../CSE5120_HW2_Submission.zip . -x "*.pyc" -x "__pycache__/*" && cd ..

echo ""
echo "✅ SUCCESS! Submission package created"
echo ""
echo "📋 Contents:"
echo "───────────"
unzip -l CSE5120_HW2_Submission.zip

echo ""
echo "📊 File sizes:"
du -h CSE5120_HW2_Submission.zip

echo ""
echo "🎉 Ready to submit to Canvas!"
echo ""
