"""
Color and styling system for Flite CLI
Professional terminal colors and formatting
"""

import os
import sys
from colorama import init, Fore, Back, Style

# Initialize colorama for cross-platform color support
init(autoreset=True)

# Detect if we're on Windows and handle Unicode issues
IS_WINDOWS = os.name == 'nt'
HAS_UNICODE_SUPPORT = True

# Check if Windows console supports Unicode
if IS_WINDOWS:
    try:
        # Try to set UTF-8 encoding for Windows console
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        elif hasattr(sys.stdout, 'encoding'):
            # Check if current encoding supports Unicode
            test_char = '✓'
            try:
                test_char.encode(sys.stdout.encoding)
            except UnicodeEncodeError:
                HAS_UNICODE_SUPPORT = False
    except:
        HAS_UNICODE_SUPPORT = False

class Colors:
    """Terminal color constants"""
    # Text colors
    RED = Fore.RED
    GREEN = Fore.GREEN
    BLUE = Fore.BLUE
    YELLOW = Fore.YELLOW
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    BLACK = Fore.BLACK
    
    # Bright colors
    BRIGHT_RED = Fore.LIGHTRED_EX
    BRIGHT_GREEN = Fore.LIGHTGREEN_EX
    BRIGHT_BLUE = Fore.LIGHTBLUE_EX
    BRIGHT_YELLOW = Fore.LIGHTYELLOW_EX
    BRIGHT_MAGENTA = Fore.LIGHTMAGENTA_EX
    BRIGHT_CYAN = Fore.LIGHTCYAN_EX
    BRIGHT_WHITE = Fore.LIGHTWHITE_EX
    
    # Background colors
    BG_RED = Back.RED
    BG_GREEN = Back.GREEN
    BG_BLUE = Back.BLUE
    BG_YELLOW = Back.YELLOW
    BG_MAGENTA = Back.MAGENTA
    BG_CYAN = Back.CYAN
    BG_WHITE = Back.WHITE
    BG_BLACK = Back.BLACK
    
    # Styles
    BOLD = Style.BRIGHT
    DIM = Style.DIM
    RESET = Style.RESET_ALL

class UI:
    """UI components and styling functions"""
    
    @staticmethod
    def header(text, width=None):
        """Create a styled header"""
        if width is None:
            width = max(80, len(text) + 4)  # Auto-adjust width based on text length
        
        if HAS_UNICODE_SUPPORT:
            border = "═" * width
            padding = (width - len(text) - 2) // 2
            remaining_space = width - len(text) - 2 - padding
            header_line = f"║{' ' * padding}{text}{' ' * remaining_space}║"
            
            return f"""
{Colors.BRIGHT_CYAN}╔{border}╗
{header_line}
╚{border}╝{Colors.RESET}"""
        else:
            border = "=" * width
            padding = (width - len(text) - 2) // 2
            remaining_space = width - len(text) - 2 - padding
            header_line = f"|{' ' * padding}{text}{' ' * remaining_space}|"
            
            return f"""
{Colors.BRIGHT_CYAN}+{border}+
{header_line}
+{border}+{Colors.RESET}"""
    
    @staticmethod
    def section_title(text):
        """Create a section title with underline"""
        underline_char = "─" if HAS_UNICODE_SUPPORT else "-"
        underline = underline_char * len(text)
        return f"\n{Colors.BRIGHT_WHITE}{Colors.BOLD}{text}{Colors.RESET}\n{Colors.CYAN}{underline}{Colors.RESET}\n"
    
    @staticmethod
    def box(content, title=None, width=60):
        """Create a content box"""
        lines = content.split('\n')
        max_content_width = max(len(line) for line in lines) if lines else 0
        box_width = max(width, max_content_width + 4, len(title) + 4 if title else 0)
        
        if HAS_UNICODE_SUPPORT:
            # Top border
            if title:
                title_padding = (box_width - len(title) - 4) // 2
                top = f"{Colors.BRIGHT_BLUE}┌─{title_padding * '─'} {Colors.BRIGHT_WHITE}{title}{Colors.BRIGHT_BLUE} {title_padding * '─'}─┐{Colors.RESET}"
            else:
                top = f"{Colors.BRIGHT_BLUE}┌{'─' * (box_width - 2)}┐{Colors.RESET}"
            
            # Content lines
            content_lines = []
            for line in lines:
                padding = box_width - len(line) - 4
                content_lines.append(f"{Colors.BRIGHT_BLUE}│{Colors.RESET} {line}{' ' * padding} {Colors.BRIGHT_BLUE}│{Colors.RESET}")
            
            # Bottom border
            bottom = f"{Colors.BRIGHT_BLUE}└{'─' * (box_width - 2)}┘{Colors.RESET}"
        else:
            # ASCII version
            if title:
                title_padding = (box_width - len(title) - 4) // 2
                top = f"{Colors.BRIGHT_BLUE}+-{title_padding * '-'} {Colors.BRIGHT_WHITE}{title}{Colors.BRIGHT_BLUE} {title_padding * '-'}-+{Colors.RESET}"
            else:
                top = f"{Colors.BRIGHT_BLUE}+{'-' * (box_width - 2)}+{Colors.RESET}"
            
            # Content lines
            content_lines = []
            for line in lines:
                padding = box_width - len(line) - 4
                content_lines.append(f"{Colors.BRIGHT_BLUE}|{Colors.RESET} {line}{' ' * padding} {Colors.BRIGHT_BLUE}|{Colors.RESET}")
            
            # Bottom border
            bottom = f"{Colors.BRIGHT_BLUE}+{'-' * (box_width - 2)}+{Colors.RESET}"
        
        return f"{top}\n" + "\n".join(content_lines) + f"\n{bottom}"
    
    @staticmethod
    def menu_item(text, selected=False, checked=None):
        """Create a styled menu item"""
        if selected:
            prefix = f"{Colors.BG_BLUE}{Colors.BRIGHT_WHITE} > "
            suffix = f" {Colors.RESET}"
            
            if checked is not None:
                if HAS_UNICODE_SUPPORT:
                    checkbox = f"{Colors.BRIGHT_GREEN}[✓]{Colors.RESET}" if checked else f"{Colors.BRIGHT_RED}[ ]{Colors.RESET}"
                else:
                    checkbox = f"{Colors.BRIGHT_GREEN}[X]{Colors.RESET}" if checked else f"{Colors.BRIGHT_RED}[ ]{Colors.RESET}"
                return f"{prefix}{checkbox} {text}{suffix}"
            else:
                return f"{prefix}{text}{suffix}"
        else:
            if checked is not None:
                if HAS_UNICODE_SUPPORT:
                    checkbox = f"{Colors.BRIGHT_GREEN}[✓]" if checked else f"{Colors.DIM}[ ]"
                else:
                    checkbox = f"{Colors.BRIGHT_GREEN}[X]" if checked else f"{Colors.DIM}[ ]"
                return f"   {checkbox}{Colors.RESET} {text}"
            else:
                return f"   {Colors.DIM}{text}{Colors.RESET}"
    
    @staticmethod
    def success(text):
        """Style success message"""
        if HAS_UNICODE_SUPPORT:
            return f"{Colors.BRIGHT_GREEN}✓ {text}{Colors.RESET}"
        else:
            return f"{Colors.BRIGHT_GREEN}[OK] {text}{Colors.RESET}"
    
    @staticmethod
    def error(text):
        """Style error message"""
        if HAS_UNICODE_SUPPORT:
            return f"{Colors.BRIGHT_RED}✗ {text}{Colors.RESET}"
        else:
            return f"{Colors.BRIGHT_RED}[ERROR] {text}{Colors.RESET}"
    
    @staticmethod
    def warning(text):
        """Style warning message"""
        if HAS_UNICODE_SUPPORT:
            return f"{Colors.BRIGHT_YELLOW}⚠ {text}{Colors.RESET}"
        else:
            return f"{Colors.BRIGHT_YELLOW}[WARNING] {text}{Colors.RESET}"
    
    @staticmethod
    def info(text):
        """Style info message"""
        if HAS_UNICODE_SUPPORT:
            return f"{Colors.BRIGHT_CYAN}ℹ {text}{Colors.RESET}"
        else:
            return f"{Colors.BRIGHT_CYAN}[INFO] {text}{Colors.RESET}"
    
    @staticmethod
    def prompt(text):
        """Style user prompt"""
        if HAS_UNICODE_SUPPORT:
            return f"{Colors.BRIGHT_WHITE}► {text}{Colors.RESET}"
        else:
            return f"{Colors.BRIGHT_WHITE}> {text}{Colors.RESET}"
    
    @staticmethod
    def highlight(text):
        """Highlight important text"""
        return f"{Colors.BRIGHT_YELLOW}{Colors.BOLD}{text}{Colors.RESET}"
    
    @staticmethod
    def dimmed(text):
        """Dimmed text for less important info"""
        return f"{Colors.DIM}{text}{Colors.RESET}"
    
    @staticmethod
    def progress_bar(current, total, width=40):
        """Create a progress bar"""
        if total == 0:
            percentage = 0
        else:
            percentage = current / total
        
        filled = int(width * percentage)
        if HAS_UNICODE_SUPPORT:
            bar = "█" * filled + "░" * (width - filled)
        else:
            bar = "=" * filled + "-" * (width - filled)
        
        return f"{Colors.BRIGHT_CYAN}[{bar}] {percentage:.1%}{Colors.RESET}"
    
    @staticmethod
    def separator(width=60, char=None):
        """Create a separator line"""
        if char is None:
            char = "─" if HAS_UNICODE_SUPPORT else "-"
        return f"{Colors.DIM}{char * width}{Colors.RESET}"
    
    @staticmethod
    def key_hint(keys, description):
        """Style keyboard shortcut hints"""
        return f"{Colors.DIM}[{Colors.BRIGHT_WHITE}{keys}{Colors.DIM}] {description}{Colors.RESET}"
    
    @staticmethod
    def logo():
        """ASCII logo for Flite"""
        if HAS_UNICODE_SUPPORT:
            return f"""{Colors.BRIGHT_RED}
    ███████╗██╗     ██╗████████╗███████╗
    ██╔════╝██║     ██║╚══██╔══╝██╔════╝
    █████╗  ██║     ██║   ██║   █████╗  
    ██╔══╝  ██║     ██║   ██║   ██╔══╝  
    ██║     ███████╗██║   ██║   ███████╗
    ╚═╝     ╚══════╝╚═╝   ╚═╝   ╚══════╝
    {Colors.BRIGHT_RED}Flask Project Generator{Colors.RESET}
    """
        else:
            return f"""{Colors.BRIGHT_RED}
    ########  ##      ##  ########  ########
    ##    ##  ##      ##  ##    ##  ##      
    ########  ##      ##  ########  ########
    ##    ##  ##      ##  ##    ##  ##      
    ########  ##########  ########  ########
    ##    ##  ##      ##  ##    ##  ##      
    {Colors.BRIGHT_RED}Flask Project Generator{Colors.RESET}
    """
