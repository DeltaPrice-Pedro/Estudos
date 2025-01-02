import 'package:flutter/material.dart';

class Login extends StatelessWidget {
  const Login(this.method, {super.key});

  final void Function() method;

  @override
  Widget build(context) {
    return Column(
      children: [
        Padding(
        padding: const EdgeInsets.only(top: 50),
        child: Image.asset(
          'assets/images/deltaprice_hori.png',
          width: 500,
        ),
      ),
        Text(
          'Bem vindo(a)\nao Delta Alimentos!',
          textAlign: TextAlign.center,
        ),
        TextButton(onPressed: method, child: Text("Trocar tela"))
      ],
    );
  }
}
