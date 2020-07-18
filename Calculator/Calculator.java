import java.awt.*;
import javax.swing.*;
import java.awt.event.*;
import javax.script.*;

public class E01 extends JFrame{
	JTextField textShow;
	JPanel panel;
	JButton buttonList[];
	
	E01(){
		init();
		setBounds(100,100,230,220);
		setTitle("欢迎");
		setVisible(true);
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		validate();
	}
	
	public void init(){
		//文本框
		textShow = new JTextField(100);
		textShow.setPreferredSize(new Dimension(200,30));
		add(textShow,BorderLayout.NORTH);
		
		//使用GridLayout布局面板放按钮
		panel = new JPanel(new GridLayout(4,4));
		buttonList = new JButton[16];
		String[] s = {"7","8","9","+","4","5","6","-","1","2","3","*","0",".","=","/"};
		for(int i = 0;i<16;i++) {
			panel.add(buttonList[i]=new JButton(s[i]));
		}
		add(panel);

		//为按钮添加监听器
		for(int i = 0;i<16;i++) {
			JButton button = buttonList[i];
			if(i!=14) {//不是等号的都显示在文本框中
				button.addActionListener(new ActionListener() {//匿名类实现接口
					public void actionPerformed(ActionEvent e) {
						textShow.setText(textShow.getText()+button.getText());//更新文本框的内容
					}
				});
			}
			else {//等号
				button.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						String s = textShow.getText();
						int indexApart=0;
						for(int i = 0;i<s.length();i++) {//找到字符串中运算符的位置
							if(s.charAt(i)=='+'||s.charAt(i)=='-'||s.charAt(i)=='*'||s.charAt(i)=='/') {
								indexApart = i;
								break;
							}
						}
						//以运算符为分界得到前后两个数的值
						double num1 = Double.parseDouble(s.substring(0,indexApart));
						double num2 = Double.parseDouble(s.substring(indexApart+1));
						double res;
						//根据运算符进行运算
						if(s.charAt(indexApart) == '+')res = num1+num2;
						else if(s.charAt(indexApart) == '-')res = num1-num2;
						else if(s.charAt(indexApart) =='*')res = num1*num2;
						else res = num1/num2;
						//如果值为整数，则显示整数
						if (Math.abs(res-Math.round(res))<1e-8)textShow.setText(String.valueOf(Math.round(res)));
						else textShow.setText(String.valueOf(res));
					}
				});
			}
		}
	}
	
	public static void main(String args[]) {
		new E01();
	}
}