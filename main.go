package main

import (
	"fmt"
	// "os"

	"charm.land/bubbles/v2/textinput"
	tea "charm.land/bubbletea/v2"
	"charm.land/lipgloss/v2"
	"log"
)

func main() {
	// fmt.Println("hello world")

	// testPass, err := term.ReadPassword(int(os.Stdin.Fd()))

	// if err != nil {
	// 	log.Fatal(err)
	// }

	// fmt.Printf("testPass: %s", testPass)

	var sessionInfo string = "test"

	clearScreen()
	p := tea.NewProgram(initialModel(sessionInfo))
	if _, err := p.Run(); err != nil {
		log.Fatal(err)
	}
}

type (
	errMsg error
)


func clearScreen() {
	fmt.Print("\033[2J\033[H")
}

type model struct {
	textInput         textinput.Model
	err               error
	quitting          bool
	sessionInfoPrompt string
}

func initialModel(sessionInfoPrompt string) model {
	ti := textinput.New()
	ti.SetVirtualCursor(false)
	ti.Focus()

	return model{
		textInput: ti,
		sessionInfoPrompt: sessionInfoPrompt,
	}
}

func (m model) Init() tea.Cmd {
	return textinput.Blink
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmd tea.Cmd

	switch msg := msg.(type) {
	case tea.KeyPressMsg:
		switch msg.String() {
		case "enter", "ctrl+c":
			m.quitting = true
			return m, tea.Quit
		}
	}
	m.textInput, cmd = m.textInput.Update(msg)
	return m, cmd
}

func (m model) View() tea.View {
	var c *tea.Cursor
	if !m.textInput.VirtualCursor() {
		c = m.textInput.Cursor()
		c.Y += lipgloss.Height(m.headerView())
	}

	str := lipgloss.JoinVertical(lipgloss.Top, m.headerView(), m.textInput.View(), m.footerView())
	if m.quitting {
		str += "\n"
	}

	v := tea.NewView(str)
	v.Cursor = c
	return v
}

func (m model) headerView() string { return m.sessionInfoPrompt + "\n" }
func (m model) footerView() string { return "\n(ctrl+c to save and quit)" }
