# coding=utf-8

"""markdown.grammars: Contains the grammars for markdown."""
import modgrammar

grammar_whitespace_mode = "optional"


class Heading(modgrammar.Grammar):
    """Defines the grammar for a heading."""
    grammar = (modgrammar.BOL, modgrammar.REPEAT(modgrammar.L("#"), min=1, max=6), modgrammar.L(" "),
               modgrammar.REST_OF_LINE)

    def grammar_elem_init(self, sessiondata):
        """Saves the headline for later use."""
        self.headline = self[3].string
        hashtags = self[1].string
        self.tag = 'h' + str(len(hashtags))


class EmptyLine(modgrammar.Grammar):
    """Defines the grammar for an empty line."""
    grammar = (modgrammar.BOL, modgrammar.EOL)


class Bold(modgrammar.Grammar):
    """Defines the grammar for bold text."""
    grammar = (modgrammar.L(" **"), modgrammar.WORD("\w \t", fullmatch=True, escapes=True), modgrammar.L("** "))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.boldText = self[1].string


class Italic(modgrammar.Grammar):
    """Defines the grammar for italic text."""
    grammar = (modgrammar.L(" *"), modgrammar.WORD("\w \t", fullmatch=True, escapes=True), modgrammar.L("* "))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.boldText = self[1].string


class Quote(modgrammar.Grammar):
    """Defines the grammar for a quote."""
    grammar = (modgrammar.BOL, modgrammar.L(">"), modgrammar.REST_OF_LINE)

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.quote = self[2].string


class ListItem(modgrammar.Grammar):
    """Defines the grammar for a list item."""
    grammar = (modgrammar.BOL, modgrammar.L("* "), modgrammar.REST_OF_LINE)

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.listItemText = self[2].string


class List(modgrammar.Grammar):
    """Defines the grammar for a list."""
    grammar = (modgrammar.LIST_OF(ListItem, sep=modgrammar.EOL))


class Text(modgrammar.Grammar):
    """Defines the grammar for normal text."""
    grammar = (modgrammar.REPEAT(modgrammar.OR(Bold, Italic, Quote,
                                               modgrammar.WORD("\w \t", escapes=True, fullmatch=True)),
                                 modgrammar.EOL, min=1))


class Paragraph(modgrammar.Grammar):
    """Defines the grammar for a paragraph."""
    grammar = (EmptyLine, Text, EmptyLine)

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.text = self[1].string


class MarkdownGrammar(modgrammar.Grammar):
    """Provides the grammar for Markdown."""
    grammar = (modgrammar.REPEAT(modgrammar.OR(Heading, Paragraph, List)))

    def grammar_elem_init(self, sessiondata):
        """Saves the text for later use."""
        self.content = self[0].string
