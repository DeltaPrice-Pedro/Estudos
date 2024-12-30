import 'package:flutter/material.dart';
import 'package:roll_dice/login/acess_widget.dart';

class Login extends StatelessWidget {
  const Login({super.key});

  @override
  Widget build(context) {
    return Column(
      children: [
        Opacity(
          opacity: 0.2,
          child: Image.asset(
            'assets/images/deltaprice_hori.png',
            width: 400,
          ),
        ),
        Text('Bem vindo(a)\nao Delta Alimentos!'),
        AcessWidget()
      ],
    );
  }
}
