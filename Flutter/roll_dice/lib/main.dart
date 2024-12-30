import 'package:flutter/material.dart';
import 'package:roll_dice/login/login.dart';
import 'package:roll_dice/menu/menu.dart';

void main() {
  runApp(const InitPage());
}

class InitPage extends StatefulWidget {
  const InitPage({super.key});

  @override
  State<InitPage> createState() {
    return _InitPage();
  }
}

class _InitPage extends State<InitPage> {
  Widget activePage = Login();

  switchPage(){
    setState(() {
      activePage = Menu();
    });
  }

  @override
  Widget build(context) {
    return MaterialApp(
        title: 'Sesas',
        home: Scaffold(
            body: Container(
          decoration: BoxDecoration(
              gradient: LinearGradient(colors: [
            const Color.fromARGB(255, 26, 131, 250),
            const Color.fromARGB(255, 74, 158, 254),
          ], begin: Alignment.topLeft, end: Alignment.bottomRight)),
          // alignment: Alignment.topCenter,
          child: Center(
            child: Column(children: [
              Padding(
                padding: const EdgeInsets.only(top: 20),
                child: Image.asset(
                  'assets/images/deltaprice_hori.png',
                  width: 400,
                ),
              ),
              activePage,
              TextButton(onPressed: switchPage, child: Text("Trocar tela"))
            ]),
          ),
        )));
  }
}
